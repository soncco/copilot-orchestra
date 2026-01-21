"""
Authentication views.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, AuditLog
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    ChangePasswordSerializer, LoginSerializer, EnableMFASerializer,
    VerifyMFASerializer, AuditLogSerializer
)
from core.common.permissions import IsAdmin
from core.common.pagination import StandardPagination


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_audit_log(user, action, resource_type, request, resource_id=None, description='', metadata=None):
    """Create audit log entry."""
    AuditLog.objects.create(
        user=user,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        metadata=metadata or {}
    )


class AuthViewSet(viewsets.GenericViewSet):
    """Authentication endpoints."""

    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        serializer = LoginSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        # Update last login
        user.last_login = timezone.now()
        user.last_login_ip = get_client_ip(request)
        user.save(update_fields=['last_login', 'last_login_ip'])

        # Create audit log
        create_audit_log(
            user=user,
            action='login',
            resource_type='auth',
            request=request,
            description='User logged in'
        )

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """User logout."""
        # Create audit log
        create_audit_log(
            user=request.user,
            action='logout',
            resource_type='auth',
            request=request,
            description='User logged out'
        )

        return Response({'message': 'Logged out successfully'})

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Refresh access token."""
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error': 'Refresh token required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token)
            })
        except Exception as e:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user."""
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update current user profile."""
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        create_audit_log(
            user=request.user,
            action='update',
            resource_type='user',
            resource_id=str(request.user.id),
            request=request,
            description='Updated profile'
        )

        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password."""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        create_audit_log(
            user=request.user,
            action='update',
            resource_type='user',
            resource_id=str(request.user.id),
            request=request,
            description='Changed password'
        )

        return Response({'message': 'Password changed successfully'})

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def enable_mfa(self, request):
        """Enable MFA for user."""
        serializer = EnableMFASerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify password
        if not request.user.check_password(serializer.validated_data['password']):
            return Response(
                {'error': 'Incorrect password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Enable MFA
        mfa_uri = request.user.enable_mfa()

        create_audit_log(
            user=request.user,
            action='update',
            resource_type='user',
            resource_id=str(request.user.id),
            request=request,
            description='Enabled MFA'
        )

        return Response({
            'mfa_uri': mfa_uri,
            'secret': request.user.mfa_secret
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def verify_mfa(self, request):
        """Verify MFA token."""
        serializer = VerifyMFASerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.verify_mfa_token(serializer.validated_data['token']):
            return Response({'valid': True})
        else:
            return Response(
                {'valid': False, 'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def disable_mfa(self, request):
        """Disable MFA for user."""
        serializer = EnableMFASerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify password
        if not request.user.check_password(serializer.validated_data['password']):
            return Response(
                {'error': 'Incorrect password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Disable MFA
        request.user.disable_mfa()

        create_audit_log(
            user=request.user,
            action='update',
            resource_type='user',
            resource_id=str(request.user.id),
            request=request,
            description='Disabled MFA'
        )

        return Response({'message': 'MFA disabled successfully'})


class UserViewSet(viewsets.ModelViewSet):
    """User management endpoints."""

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'is_active', 'mfa_enabled']
    search_fields = ['email', 'first_name', 'last_name']

    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def perform_create(self, serializer):
        """Create user and log action."""
        user = serializer.save()

        create_audit_log(
            user=self.request.user,
            action='create',
            resource_type='user',
            resource_id=str(user.id),
            request=self.request,
            description=f'Created user {user.email}'
        )

    def perform_update(self, serializer):
        """Update user and log action."""
        user = serializer.save()

        create_audit_log(
            user=self.request.user,
            action='update',
            resource_type='user',
            resource_id=str(user.id),
            request=self.request,
            description=f'Updated user {user.email}'
        )

    def perform_destroy(self, instance):
        """Soft delete user and log action."""
        instance.is_active = False
        instance.save()

        create_audit_log(
            user=self.request.user,
            action='delete',
            resource_type='user',
            resource_id=str(instance.id),
            request=self.request,
            description=f'Deactivated user {instance.email}'
        )


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Audit log endpoints (read-only)."""

    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'action', 'resource_type']

    def get_queryset(self):
        """Filter queryset based on user role."""
        queryset = super().get_queryset()

        # Non-admin users can only see their own logs
        if self.request.user.role != 'admin':
            queryset = queryset.filter(user=self.request.user)

        return queryset

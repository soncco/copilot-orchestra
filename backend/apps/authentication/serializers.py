"""
Serializers for authentication.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, AuditLog


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone', 'avatar', 'mfa_enabled', 'is_active',
            'email_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'email_verified']


class UserCreateSerializer(serializers.ModelSerializer):
    """User creation serializer."""

    password = serializers.CharField(
        write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'role',
            'phone', 'password', 'password_confirm'
        ]

    def validate(self, attrs):
        """Validate passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})
        attrs.pop('password_confirm')
        return attrs

    def create(self, validated_data):
        """Create user with hashed password."""
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **validated_data
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """User update serializer."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'avatar']


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(
        required=True, write_only=True)

    def validate(self, attrs):
        """Validate passwords."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {'new_password': 'Passwords do not match'})
        return attrs

    def validate_old_password(self, value):
        """Validate old password is correct."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Incorrect password')
        return value


class LoginSerializer(serializers.Serializer):
    """Login serializer."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    mfa_token = serializers.CharField(
        required=False, allow_blank=True, write_only=True)

    def validate(self, attrs):
        """Validate credentials."""
        username = attrs.get('username')
        password = attrs.get('password')
        mfa_token = attrs.get('mfa_token', '')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )

            if not user:
                raise serializers.ValidationError('Invalid credentials')

            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')

            # Check MFA if enabled
            if user.mfa_enabled:
                if not mfa_token:
                    raise serializers.ValidationError('MFA token required')
                if not user.verify_mfa_token(mfa_token):
                    raise serializers.ValidationError('Invalid MFA token')

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include username and password')


class EnableMFASerializer(serializers.Serializer):
    """Enable MFA serializer."""

    password = serializers.CharField(required=True, write_only=True)


class VerifyMFASerializer(serializers.Serializer):
    """Verify MFA token serializer."""

    token = serializers.CharField(required=True, max_length=6, min_length=6)


class AuditLogSerializer(serializers.ModelSerializer):
    """Audit log serializer."""

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_email', 'action', 'resource_type',
            'resource_id', 'description', 'ip_address', 'user_agent',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

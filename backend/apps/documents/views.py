"""
Documents views.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from core.common.permissions import IsAuthenticated
from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """Document ViewSet with file upload support."""

    queryset = Document.objects.select_related(
        'group', 'passenger', 'supplier', 'uploaded_by'
    ).all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'document_type', 'related_to', 'group', 'passenger',
        'supplier', 'is_public', 'is_archived'
    ]
    search_fields = ['name', 'description', 'tags', 'notes']
    ordering_fields = ['created_at', 'name', 'expires_at', 'file_size']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer for action."""
        if self.action in ['create', 'upload']:
            return DocumentUploadSerializer
        return DocumentSerializer

    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = super().get_queryset()

        # Non-admin users only see public documents or their own uploads
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                models.Q(is_public=True) | models.Q(
                    uploaded_by=self.request.user)
            )

        # Filter archived documents unless explicitly requested
        if not self.request.query_params.get('show_archived'):
            queryset = queryset.filter(is_archived=False)

        return queryset

    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload a new document."""
        serializer = DocumentUploadSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        document = serializer.save()

        return Response(
            DocumentSerializer(document, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive a document."""
        document = self.get_object()
        document.is_archived = True
        document.save()

        return Response(DocumentSerializer(document, context={'request': request}).data)

    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        """Unarchive a document."""
        document = self.get_object()
        document.is_archived = False
        document.save()

        return Response(DocumentSerializer(document, context={'request': request}).data)

    @action(detail=False, methods=['get'])
    def by_group(self, request):
        """Get all documents for a group."""
        group_id = request.query_params.get('group_id')

        if not group_id:
            return Response(
                {'error': 'group_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        documents = self.get_queryset().filter(group_id=group_id)
        serializer = self.get_serializer(documents, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_passenger(self, request):
        """Get all documents for a passenger."""
        passenger_id = request.query_params.get('passenger_id')

        if not passenger_id:
            return Response(
                {'error': 'passenger_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        documents = self.get_queryset().filter(passenger_id=passenger_id)
        serializer = self.get_serializer(documents, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get documents expiring in the next 30 days."""
        days = int(request.query_params.get('days', 30))

        today = timezone.now().date()
        future_date = today + timezone.timedelta(days=days)

        documents = self.get_queryset().filter(
            expires_at__gte=today,
            expires_at__lte=future_date
        ).order_by('expires_at')

        serializer = self.get_serializer(documents, many=True)

        return Response({
            'days': days,
            'count': documents.count(),
            'documents': serializer.data
        })

    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Get expired documents."""
        today = timezone.now().date()

        documents = self.get_queryset().filter(
            expires_at__lt=today
        ).order_by('expires_at')

        serializer = self.get_serializer(documents, many=True)

        return Response({
            'count': documents.count(),
            'documents': serializer.data
        })

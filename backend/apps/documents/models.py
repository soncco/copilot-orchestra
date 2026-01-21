"""
Documents models.
"""
from django.db import models
from django.core.validators import FileExtensionValidator
from core.common.models import TimeStampedModel
from apps.circuits.models import Group, Passenger
from apps.suppliers.models import Supplier


class Document(TimeStampedModel):
    """Documents storage (contracts, invoices, travel docs, etc.)."""
    
    DOCUMENT_TYPE_CHOICES = [
        ('contract', 'Contract'),
        ('invoice', 'Invoice'),
        ('receipt', 'Receipt'),
        ('passport', 'Passport'),
        ('visa', 'Visa'),
        ('insurance', 'Insurance'),
        ('itinerary', 'Itinerary'),
        ('voucher', 'Voucher'),
        ('ticket', 'Ticket'),
        ('photo', 'Photo'),
        ('report', 'Report'),
        ('other', 'Other'),
    ]
    
    RELATED_TO_CHOICES = [
        ('group', 'Group'),
        ('passenger', 'Passenger'),
        ('supplier', 'Supplier'),
        ('general', 'General'),
    ]
    
    # Document details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    
    # File
    file = models.FileField(
        upload_to='documents/%Y/%m/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'pdf', 'doc', 'docx', 'xls', 'xlsx',
                    'jpg', 'jpeg', 'png', 'gif',
                    'txt', 'csv', 'zip'
                ]
            )
        ]
    )
    file_size = models.IntegerField(help_text='File size in bytes', null=True, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)
    
    # Related to
    related_to = models.CharField(max_length=20, choices=RELATED_TO_CHOICES)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True
    )
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True
    )
    
    # Metadata
    uploaded_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents'
    )
    tags = models.JSONField(default=list, blank=True, help_text='Document tags')
    
    # Access control
    is_public = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    # Expiration (for passports, visas, insurance, etc.)
    expires_at = models.DateField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'documents'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['document_type', 'related_to']),
            models.Index(fields=['group', 'document_type']),
            models.Index(fields=['passenger', 'document_type']),
            models.Index(fields=['supplier', 'document_type']),
            models.Index(fields=['is_archived', 'created_at']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.document_type})"
    
    def save(self, *args, **kwargs):
        """Set file size and validate related_to."""
        if self.file:
            self.file_size = self.file.size
        
        # Validate related_to matches the foreign key
        if self.related_to == 'group' and not self.group:
            raise ValueError('Group is required when related_to is "group"')
        elif self.related_to == 'passenger' and not self.passenger:
            raise ValueError('Passenger is required when related_to is "passenger"')
        elif self.related_to == 'supplier' and not self.supplier:
            raise ValueError('Supplier is required when related_to is "supplier"')
        
        super().save(*args, **kwargs)
    
    @property
    def file_url(self):
        """Get file URL."""
        if self.file:
            return self.file.url
        return None
    
    @property
    def is_expired(self):
        """Check if document is expired."""
        if self.expires_at:
            from django.utils import timezone
            return self.expires_at < timezone.now().date()
        return False

"""
Documents admin configuration.
"""
from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Document admin."""

    list_display = [
        'name', 'document_type', 'related_to',
        'file_size_display', 'uploaded_by',
        'is_public', 'is_archived', 'expires_at',
        'created_at'
    ]
    list_filter = [
        'document_type', 'related_to', 'is_public',
        'is_archived', 'created_at', 'expires_at'
    ]
    search_fields = [
        'name', 'description', 'notes',
        'group__code', 'passenger__first_name',
        'passenger__last_name', 'supplier__name'
    ]
    readonly_fields = [
        'file_size', 'mime_type', 'uploaded_by',
        'file_url', 'is_expired', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Document Info', {
            'fields': ('name', 'description', 'document_type')
        }),
        ('File', {
            'fields': ('file', 'file_url', 'file_size', 'mime_type')
        }),
        ('Related To', {
            'fields': ('related_to', 'group', 'passenger', 'supplier')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'tags', 'is_public', 'is_archived')
        }),
        ('Expiration', {
            'fields': ('expires_at', 'is_expired')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def file_size_display(self, obj):
        """Display file size in human-readable format."""
        if not obj.file_size:
            return '-'

        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    file_size_display.short_description = 'File Size'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'group', 'passenger', 'supplier', 'uploaded_by'
        )

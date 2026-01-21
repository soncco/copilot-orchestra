"""
Documents serializers.
"""
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """Document serializer."""

    file_url = serializers.SerializerMethodField()
    uploaded_by_name = serializers.CharField(
        source='uploaded_by.get_full_name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    # Related entity names
    group_code = serializers.CharField(source='group.code', read_only=True)
    passenger_name = serializers.CharField(
        source='passenger.full_name', read_only=True)
    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'name', 'description', 'document_type',
            'file', 'file_url', 'file_size', 'mime_type',
            'related_to', 'group', 'group_code',
            'passenger', 'passenger_name',
            'supplier', 'supplier_name',
            'uploaded_by', 'uploaded_by_name',
            'tags', 'is_public', 'is_archived',
            'expires_at', 'is_expired', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'file_size',
                            'uploaded_by', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        """Get file URL."""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None

    def validate(self, data):
        """Validate related_to matches foreign keys."""
        related_to = data.get('related_to')

        if related_to == 'group' and not data.get('group'):
            raise serializers.ValidationError({
                'group': 'Group is required when related_to is "group"'
            })
        elif related_to == 'passenger' and not data.get('passenger'):
            raise serializers.ValidationError({
                'passenger': 'Passenger is required when related_to is "passenger"'
            })
        elif related_to == 'supplier' and not data.get('supplier'):
            raise serializers.ValidationError({
                'supplier': 'Supplier is required when related_to is "supplier"'
            })

        # Clear other foreign keys
        if related_to != 'group':
            data['group'] = None
        if related_to != 'passenger':
            data['passenger'] = None
        if related_to != 'supplier':
            data['supplier'] = None

        return data

    def create(self, validated_data):
        """Set uploaded_by from request user."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['uploaded_by'] = request.user
        return super().create(validated_data)


class DocumentUploadSerializer(serializers.ModelSerializer):
    """Simplified serializer for document upload."""

    class Meta:
        model = Document
        fields = [
            'name', 'description', 'document_type', 'file',
            'related_to', 'group', 'passenger', 'supplier',
            'tags', 'is_public', 'expires_at', 'notes'
        ]

    def create(self, validated_data):
        """Set uploaded_by and detect mime_type."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['uploaded_by'] = request.user

        # Try to get mime type from uploaded file
        file = validated_data.get('file')
        if file and hasattr(file, 'content_type'):
            validated_data['mime_type'] = file.content_type

        return super().create(validated_data)

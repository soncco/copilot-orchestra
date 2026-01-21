"""
Serializers for suppliers app.
"""
from rest_framework import serializers
from .models import Supplier, SupplierService, PricePeriod, ExchangeRate


class SupplierSerializer(serializers.ModelSerializer):
    """Supplier serializer."""

    services_count = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = [
            'id', 'code', 'name', 'supplier_type', 'status',
            'contact_name', 'email', 'phone', 'address', 'city', 'country',
            'tax_id', 'payment_terms', 'bank_account', 'rating', 'notes',
            'services_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_services_count(self, obj):
        """Get count of active services."""
        return obj.services.filter(is_active=True).count()


class PricePeriodSerializer(serializers.ModelSerializer):
    """Price period serializer."""

    class Meta:
        model = PricePeriod
        fields = [
            'id', 'service', 'season', 'start_date', 'end_date',
            'price', 'currency', 'min_stay', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate date range."""
        if attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date'
            })
        return attrs


class SupplierServiceSerializer(serializers.ModelSerializer):
    """Supplier service serializer."""

    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True)
    price_periods = PricePeriodSerializer(many=True, read_only=True)

    class Meta:
        model = SupplierService
        fields = [
            'id', 'supplier', 'supplier_name', 'service_type', 'name',
            'description', 'base_price', 'currency', 'unit',
            'is_active', 'min_quantity', 'max_quantity', 'notes',
            'price_periods', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupplierServiceCreateSerializer(serializers.ModelSerializer):
    """Supplier service creation serializer."""

    class Meta:
        model = SupplierService
        fields = [
            'supplier', 'service_type', 'name', 'description',
            'base_price', 'currency', 'unit', 'is_active',
            'min_quantity', 'max_quantity', 'notes'
        ]


class ExchangeRateSerializer(serializers.ModelSerializer):
    """Exchange rate serializer."""

    class Meta:
        model = ExchangeRate
        fields = [
            'id', 'from_currency', 'to_currency', 'rate', 'date',
            'source', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate currencies are different."""
        if attrs['from_currency'] == attrs['to_currency']:
            raise serializers.ValidationError({
                'to_currency': 'From and to currencies must be different'
            })
        return attrs


class ConvertCurrencySerializer(serializers.Serializer):
    """Serializer for currency conversion."""

    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=True)
    from_currency = serializers.CharField(max_length=3, required=True)
    to_currency = serializers.CharField(max_length=3, required=True)
    date = serializers.DateField(required=False)

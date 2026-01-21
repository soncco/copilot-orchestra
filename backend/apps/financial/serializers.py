"""
Financial serializers.
"""
from rest_framework import serializers
from .models import GroupCost, AdditionalSale, Commission, Invoice, BankDeposit


class GroupCostSerializer(serializers.ModelSerializer):
    """GroupCost serializer."""

    group_code = serializers.CharField(source='group.code', read_only=True)
    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True)

    class Meta:
        model = GroupCost
        fields = [
            'id', 'group', 'group_code', 'supplier', 'supplier_name',
            'cost_type', 'description', 'quantity', 'unit_price',
            'total_amount', 'currency', 'includes_tax', 'tax_amount',
            'paid', 'payment_date', 'invoice_number', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate payment date."""
        if data.get('paid') and not data.get('payment_date'):
            raise serializers.ValidationError({
                'payment_date': 'Payment date is required when cost is marked as paid.'
            })
        return data


class AdditionalSaleSerializer(serializers.ModelSerializer):
    """AdditionalSale serializer."""

    passenger_name = serializers.CharField(
        source='passenger.full_name', read_only=True)

    class Meta:
        model = AdditionalSale
        fields = [
            'id', 'passenger', 'passenger_name',
            'sale_type', 'description', 'quantity', 'unit_price',
            'total_amount', 'currency', 'includes_tax', 'tax_amount',
            'paid', 'payment_method', 'payment_date',
            'invoice_number', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate payment info."""
        if data.get('paid'):
            if not data.get('payment_date'):
                raise serializers.ValidationError({
                    'payment_date': 'Payment date is required when sale is marked as paid.'
                })
            if not data.get('payment_method'):
                raise serializers.ValidationError({
                    'payment_method': 'Payment method is required when sale is marked as paid.'
                })
        return data


class CommissionSerializer(serializers.ModelSerializer):
    """Commission serializer."""

    group_code = serializers.CharField(source='group.code', read_only=True)

    class Meta:
        model = Commission
        fields = [
            'id', 'group', 'group_code',
            'commission_type', 'recipient_name', 'recipient_email',
            'percentage', 'base_amount', 'commission_amount', 'currency',
            'paid', 'payment_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_percentage(self, value):
        """Validate percentage is between 0 and 100."""
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                'Percentage must be between 0 and 100.')
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    """Invoice serializer."""

    passenger_name = serializers.CharField(
        source='passenger.full_name', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'passenger', 'passenger_name',
            'invoice_type', 'invoice_number', 'issue_date', 'due_date',
            'status', 'customer_name', 'customer_document_type',
            'customer_document_number', 'customer_address', 'customer_email',
            'subtotal', 'tax_amount', 'total_amount', 'currency',
            'paid', 'payment_date', 'payment_method',
            'sunat_response', 'xml_file', 'pdf_file', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate invoice amounts."""
        if 'subtotal' in data and 'tax_amount' in data and 'total_amount' in data:
            expected_total = data['subtotal'] + data['tax_amount']
            if abs(expected_total - data['total_amount']) > 0.01:
                raise serializers.ValidationError({
                    'total_amount': 'Total amount must equal subtotal + tax amount.'
                })

        if data.get('status') in ['sent', 'accepted'] and not data.get('sunat_response'):
            raise serializers.ValidationError({
                'sunat_response': 'SUNAT response is required for sent/accepted invoices.'
            })

        return data


class InvoiceCreateSerializer(serializers.ModelSerializer):
    """Invoice create serializer with automatic calculations."""

    class Meta:
        model = Invoice
        fields = [
            'passenger', 'invoice_type', 'invoice_number', 'issue_date', 'due_date',
            'customer_name', 'customer_document_type', 'customer_document_number',
            'customer_address', 'customer_email', 'subtotal', 'currency', 'notes'
        ]

    def create(self, validated_data):
        """Create invoice with automatic tax calculation."""
        subtotal = validated_data['subtotal']

        # Calculate IGV (18% in Peru)
        tax_amount = subtotal * 0.18
        total_amount = subtotal + tax_amount

        validated_data['tax_amount'] = tax_amount
        validated_data['total_amount'] = total_amount

        return super().create(validated_data)


class BankDepositSerializer(serializers.ModelSerializer):
    """BankDeposit serializer."""

    group_code = serializers.CharField(source='group.code', read_only=True)
    passenger_name = serializers.CharField(
        source='passenger.full_name', read_only=True)
    verified_by_name = serializers.CharField(
        source='verified_by.get_full_name', read_only=True)

    class Meta:
        model = BankDeposit
        fields = [
            'id', 'group', 'group_code', 'passenger', 'passenger_name',
            'deposit_date', 'payment_method', 'amount', 'currency',
            'bank_name', 'account_number', 'reference_number',
            'status', 'verified_by', 'verified_by_name', 'verified_at',
            'receipt_file', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'verified_by',
                            'verified_at', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate deposit info."""
        if data.get('payment_method') in ['transfer', 'deposit']:
            if not data.get('bank_name'):
                raise serializers.ValidationError({
                    'bank_name': 'Bank name is required for transfers and deposits.'
                })
        return data

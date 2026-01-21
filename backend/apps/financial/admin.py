"""
Financial admin configuration.
"""
from django.contrib import admin
from .models import GroupCost, AdditionalSale, Commission, Invoice, BankDeposit


@admin.register(GroupCost)
class GroupCostAdmin(admin.ModelAdmin):
    """GroupCost admin."""

    list_display = [
        'group', 'cost_type', 'description', 'total_amount',
        'currency', 'paid', 'payment_date', 'supplier'
    ]
    list_filter = ['cost_type', 'paid', 'currency', 'includes_tax']
    search_fields = ['group__code', 'description', 'invoice_number']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'payment_date'

    fieldsets = (
        ('Group & Supplier', {
            'fields': ('group', 'supplier')
        }),
        ('Cost Details', {
            'fields': (
                'cost_type', 'description', 'quantity',
                'unit_price', 'total_amount', 'currency'
            )
        }),
        ('Tax', {
            'fields': ('includes_tax', 'tax_amount')
        }),
        ('Payment', {
            'fields': ('paid', 'payment_date', 'invoice_number')
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


@admin.register(AdditionalSale)
class AdditionalSaleAdmin(admin.ModelAdmin):
    """AdditionalSale admin."""

    list_display = [
        'passenger', 'sale_type', 'description', 'total_amount',
        'currency', 'paid', 'payment_date'
    ]
    list_filter = ['sale_type', 'paid', 'currency', 'payment_method']
    search_fields = ['passenger__first_name',
                     'passenger__last_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'payment_date'

    fieldsets = (
        ('Passenger', {
            'fields': ('passenger',)
        }),
        ('Sale Details', {
            'fields': (
                'sale_type', 'description', 'quantity',
                'unit_price', 'total_amount', 'currency'
            )
        }),
        ('Tax', {
            'fields': ('includes_tax', 'tax_amount')
        }),
        ('Payment', {
            'fields': ('paid', 'payment_method', 'payment_date', 'invoice_number')
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


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    """Commission admin."""

    list_display = [
        'group', 'commission_type', 'recipient_name',
        'percentage', 'commission_amount', 'currency',
        'paid', 'payment_date'
    ]
    list_filter = ['commission_type', 'paid', 'currency']
    search_fields = ['group__code', 'recipient_name', 'recipient_email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'payment_date'

    fieldsets = (
        ('Group', {
            'fields': ('group',)
        }),
        ('Recipient', {
            'fields': ('commission_type', 'recipient_name', 'recipient_email')
        }),
        ('Commission Calculation', {
            'fields': ('percentage', 'base_amount', 'commission_amount', 'currency')
        }),
        ('Payment', {
            'fields': ('paid', 'payment_date')
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


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Invoice admin."""

    list_display = [
        'invoice_number', 'invoice_type', 'customer_name',
        'issue_date', 'total_amount', 'currency',
        'status', 'paid'
    ]
    list_filter = ['invoice_type', 'status', 'paid', 'currency']
    search_fields = [
        'invoice_number', 'customer_name',
        'customer_document_number', 'passenger__first_name',
        'passenger__last_name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'issue_date'

    fieldsets = (
        ('Invoice Info', {
            'fields': (
                'passenger', 'invoice_type', 'invoice_number',
                'issue_date', 'due_date', 'status'
            )
        }),
        ('Customer Info', {
            'fields': (
                'customer_name', 'customer_document_type',
                'customer_document_number', 'customer_address',
                'customer_email'
            )
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'total_amount', 'currency')
        }),
        ('Payment', {
            'fields': ('paid', 'payment_date', 'payment_method')
        }),
        ('SUNAT', {
            'fields': ('sunat_response', 'xml_file', 'pdf_file'),
            'classes': ('collapse',)
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


@admin.register(BankDeposit)
class BankDepositAdmin(admin.ModelAdmin):
    """BankDeposit admin."""

    list_display = [
        'group', 'passenger', 'deposit_date',
        'amount', 'currency', 'payment_method',
        'status', 'verified_by'
    ]
    list_filter = ['payment_method', 'status', 'currency', 'deposit_date']
    search_fields = [
        'group__code', 'reference_number', 'bank_name',
        'passenger__first_name', 'passenger__last_name'
    ]
    readonly_fields = ['verified_by',
                       'verified_at', 'created_at', 'updated_at']
    date_hierarchy = 'deposit_date'

    fieldsets = (
        ('Group & Passenger', {
            'fields': ('group', 'passenger')
        }),
        ('Deposit Details', {
            'fields': (
                'deposit_date', 'payment_method',
                'amount', 'currency'
            )
        }),
        ('Bank Info', {
            'fields': ('bank_name', 'account_number', 'reference_number')
        }),
        ('Verification', {
            'fields': ('status', 'verified_by', 'verified_at')
        }),
        ('Receipt', {
            'fields': ('receipt_file',)
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

"""
Admin configuration for suppliers app.
"""
from django.contrib import admin
from .models import Supplier, SupplierService, PricePeriod, ExchangeRate


class SupplierServiceInline(admin.TabularInline):
    """Inline services for supplier admin."""
    model = SupplierService
    extra = 0
    fields = ['service_type', 'name', 'base_price', 'currency', 'is_active']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Supplier admin configuration."""

    list_display = [
        'code', 'name', 'supplier_type', 'status',
        'city', 'country', 'rating'
    ]
    list_filter = ['supplier_type', 'status', 'country']
    search_fields = ['code', 'name', 'contact_name', 'email', 'tax_id']
    ordering = ['name']
    inlines = [SupplierServiceInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'supplier_type', 'status')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'email', 'phone', 'address', 'city', 'country')
        }),
        ('Tax & Payment', {
            'fields': ('tax_id', 'payment_terms', 'bank_account')
        }),
        ('Rating & Notes', {
            'fields': ('rating', 'notes')
        }),
    )


class PricePeriodInline(admin.TabularInline):
    """Inline price periods for service admin."""
    model = PricePeriod
    extra = 0
    fields = ['season', 'start_date', 'end_date', 'price', 'currency']


@admin.register(SupplierService)
class SupplierServiceAdmin(admin.ModelAdmin):
    """Supplier service admin configuration."""

    list_display = [
        'name', 'supplier', 'service_type', 'base_price',
        'currency', 'is_active'
    ]
    list_filter = ['service_type', 'is_active', 'currency']
    search_fields = ['name', 'description', 'supplier__name']
    ordering = ['supplier', 'name']
    inlines = [PricePeriodInline]


@admin.register(PricePeriod)
class PricePeriodAdmin(admin.ModelAdmin):
    """Price period admin configuration."""

    list_display = [
        'service', 'season', 'start_date', 'end_date',
        'price', 'currency'
    ]
    list_filter = ['season', 'currency']
    search_fields = ['service__name']
    ordering = ['service', 'start_date']


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    """Exchange rate admin configuration."""

    list_display = [
        'from_currency', 'to_currency', 'rate', 'date', 'source'
    ]
    list_filter = ['from_currency', 'to_currency', 'date']
    search_fields = ['from_currency', 'to_currency', 'source']
    ordering = ['-date', 'from_currency']

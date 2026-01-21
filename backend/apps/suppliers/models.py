"""
Suppliers models: Supplier, SupplierService, PricePeriod, ExchangeRate.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.common.models import TimeStampedModel


class Supplier(TimeStampedModel):
    """Supplier (hotels, restaurants, transport, guides, etc.)."""

    TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('transport', 'Transport'),
        ('guide', 'Guide'),
        ('attraction', 'Attraction'),
        ('insurance', 'Insurance'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    ]

    # Basic info
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    supplier_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active')

    # Contact info
    contact_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=3, default='PER')

    # Tax info
    tax_id = models.CharField(
        max_length=20, blank=True, help_text='RUC or Tax ID')

    # Payment
    payment_terms = models.CharField(
        max_length=100, blank=True, help_text='e.g., Net 30')
    bank_account = models.CharField(max_length=100, blank=True)

    # Rating and notes
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'suppliers'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['supplier_type', 'status']),
            models.Index(fields=['country', 'city']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class SupplierService(TimeStampedModel):
    """Services provided by suppliers."""

    SERVICE_TYPE_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('meal', 'Meal'),
        ('transport', 'Transport'),
        ('guide', 'Guide Service'),
        ('entrance', 'Entrance Fee'),
        ('activity', 'Activity'),
        ('other', 'Other'),
    ]

    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name='services')
    service_type = models.CharField(
        max_length=20, choices=SERVICE_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    unit = models.CharField(max_length=50, blank=True,
                            help_text='e.g., per person, per night')

    # Availability
    is_active = models.BooleanField(default=True)
    min_quantity = models.IntegerField(default=1)
    max_quantity = models.IntegerField(null=True, blank=True)

    # Details
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'supplier_services'
        verbose_name = 'Supplier Service'
        verbose_name_plural = 'Supplier Services'
        ordering = ['supplier', 'name']
        indexes = [
            models.Index(fields=['supplier', 'service_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.supplier.name} - {self.name}"


class PricePeriod(TimeStampedModel):
    """Seasonal pricing for supplier services."""

    SEASON_CHOICES = [
        ('low', 'Low Season'),
        ('mid', 'Mid Season'),
        ('high', 'High Season'),
        ('peak', 'Peak Season'),
    ]

    service = models.ForeignKey(
        SupplierService, on_delete=models.CASCADE, related_name='price_periods')
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)

    # Date range
    start_date = models.DateField()
    end_date = models.DateField()

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Conditions
    min_stay = models.IntegerField(
        null=True, blank=True, help_text='Minimum nights/days')
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'price_periods'
        verbose_name = 'Price Period'
        verbose_name_plural = 'Price Periods'
        ordering = ['service', 'start_date']
        indexes = [
            models.Index(fields=['service', 'start_date', 'end_date']),
            models.Index(fields=['season']),
        ]

    def __str__(self):
        return f"{self.service.name} - {self.season} ({self.start_date} to {self.end_date})"


class ExchangeRate(TimeStampedModel):
    """Exchange rates for currency conversion."""

    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=12, decimal_places=6)
    date = models.DateField()

    # Source
    source = models.CharField(
        max_length=100, blank=True, help_text='e.g., SUNAT, BCR')

    class Meta:
        db_table = 'exchange_rates'
        verbose_name = 'Exchange Rate'
        verbose_name_plural = 'Exchange Rates'
        ordering = ['-date', 'from_currency']
        indexes = [
            models.Index(fields=['from_currency', 'to_currency', 'date']),
            models.Index(fields=['date']),
        ]
        unique_together = ['from_currency', 'to_currency', 'date']

    def __str__(self):
        return f"{self.from_currency}/{self.to_currency}: {self.rate} ({self.date})"

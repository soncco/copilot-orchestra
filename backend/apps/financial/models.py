"""
Financial models: GroupCost, AdditionalSale, Commission, Invoice, BankDeposit.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.common.models import TimeStampedModel
from apps.circuits.models import Group, Passenger
from apps.suppliers.models import Supplier


class GroupCost(TimeStampedModel):
    """Costs associated with a group."""

    COST_TYPE_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('transport', 'Transport'),
        ('meals', 'Meals'),
        ('guide', 'Guide'),
        ('entrance', 'Entrance Fees'),
        ('insurance', 'Insurance'),
        ('commission', 'Commission'),
        ('other', 'Other'),
    ]

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='costs')
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='group_costs',
        null=True,
        blank=True
    )

    # Cost details
    cost_type = models.CharField(max_length=20, choices=COST_TYPE_CHOICES)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(
        default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Tax
    includes_tax = models.BooleanField(default=False)
    tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    # Payment
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    # Reference
    invoice_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'group_costs'
        verbose_name = 'Group Cost'
        verbose_name_plural = 'Group Costs'
        ordering = ['group', '-created_at']
        indexes = [
            models.Index(fields=['group', 'cost_type']),
            models.Index(fields=['supplier', 'paid']),
            models.Index(fields=['paid', 'payment_date']),
        ]

    def __str__(self):
        return f"{self.group.code} - {self.description}"

    def save(self, *args, **kwargs):
        """Calculate total amount if not set."""
        if not self.total_amount:
            self.total_amount = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class AdditionalSale(TimeStampedModel):
    """Additional sales to passengers (extras, upgrades, etc.)."""

    SALE_TYPE_CHOICES = [
        ('upgrade', 'Room Upgrade'),
        ('excursion', 'Extra Excursion'),
        ('meal', 'Extra Meal'),
        ('souvenir', 'Souvenir'),
        ('transfer', 'Extra Transfer'),
        ('other', 'Other'),
    ]

    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, related_name='additional_sales')

    # Sale details
    sale_type = models.CharField(max_length=20, choices=SALE_TYPE_CHOICES)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(
        default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Tax
    includes_tax = models.BooleanField(default=True)
    tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    # Payment
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True)
    payment_date = models.DateField(null=True, blank=True)

    # Reference
    invoice_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'additional_sales'
        verbose_name = 'Additional Sale'
        verbose_name_plural = 'Additional Sales'
        ordering = ['passenger', '-created_at']
        indexes = [
            models.Index(fields=['passenger', 'sale_type']),
            models.Index(fields=['paid', 'payment_date']),
        ]

    def __str__(self):
        return f"{self.passenger.full_name} - {self.description}"

    def save(self, *args, **kwargs):
        """Calculate total amount and tax if not set."""
        if not self.total_amount:
            self.total_amount = self.unit_price * self.quantity

        if self.includes_tax and not self.tax_amount:
            # Calculate IGV (18% in Peru)
            base = self.total_amount / 1.18
            self.tax_amount = self.total_amount - base

        super().save(*args, **kwargs)


class Commission(TimeStampedModel):
    """Sales commissions."""

    COMMISSION_TYPE_CHOICES = [
        ('agent', 'Travel Agent'),
        ('referral', 'Referral'),
        ('guide', 'Guide'),
        ('other', 'Other'),
    ]

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='commissions')

    # Commission details
    commission_type = models.CharField(
        max_length=20, choices=COMMISSION_TYPE_CHOICES)
    recipient_name = models.CharField(max_length=200)
    recipient_email = models.EmailField(blank=True)

    # Calculation
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Commission percentage'
    )
    base_amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Payment
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    # Reference
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'commissions'
        verbose_name = 'Commission'
        verbose_name_plural = 'Commissions'
        ordering = ['group', '-created_at']
        indexes = [
            models.Index(fields=['group', 'commission_type']),
            models.Index(fields=['paid', 'payment_date']),
            models.Index(fields=['recipient_email']),
        ]

    def __str__(self):
        return f"{self.recipient_name} - {self.group.code}"

    def save(self, *args, **kwargs):
        """Calculate commission amount if not set."""
        if not self.commission_amount:
            self.commission_amount = (self.base_amount * self.percentage) / 100
        super().save(*args, **kwargs)


class Invoice(TimeStampedModel):
    """Invoices for passengers (SUNAT electronic invoicing)."""

    INVOICE_TYPE_CHOICES = [
        ('boleta', 'Boleta de Venta'),
        ('factura', 'Factura'),
        ('nota_credito', 'Nota de Crédito'),
        ('nota_debito', 'Nota de Débito'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('sent', 'Sent to SUNAT'),
        ('accepted', 'Accepted by SUNAT'),
        ('rejected', 'Rejected by SUNAT'),
        ('cancelled', 'Cancelled'),
    ]

    passenger = models.ForeignKey(
        Passenger, on_delete=models.PROTECT, related_name='invoices')

    # Invoice details
    invoice_type = models.CharField(
        max_length=20, choices=INVOICE_TYPE_CHOICES)
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)

    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='draft')

    # Customer info
    customer_name = models.CharField(max_length=200)
    customer_document_type = models.CharField(max_length=20)
    customer_document_number = models.CharField(max_length=50)
    customer_address = models.TextField(blank=True)
    customer_email = models.EmailField(blank=True)

    # Amounts
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='PEN')

    # Payment
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)

    # SUNAT
    sunat_response = models.JSONField(default=dict, blank=True)
    xml_file = models.FileField(
        upload_to='invoices/xml/', blank=True, null=True)
    pdf_file = models.FileField(
        upload_to='invoices/pdf/', blank=True, null=True)

    # Notes
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-issue_date', '-invoice_number']
        indexes = [
            models.Index(fields=['passenger', 'status']),
            models.Index(fields=['invoice_number']),
            models.Index(fields=['status', 'issue_date']),
            models.Index(fields=['customer_document_number']),
        ]

    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"


class BankDeposit(TimeStampedModel):
    """Bank deposits/payments from clients."""

    PAYMENT_METHOD_CHOICES = [
        ('transfer', 'Bank Transfer'),
        ('deposit', 'Bank Deposit'),
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='bank_deposits')
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        related_name='bank_deposits',
        null=True,
        blank=True
    )

    # Deposit details
    deposit_date = models.DateField()
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Bank info
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)

    # Verification
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_deposits'
    )
    verified_at = models.DateTimeField(null=True, blank=True)

    # Receipt
    receipt_file = models.FileField(
        upload_to='deposits/', blank=True, null=True)

    # Notes
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'bank_deposits'
        verbose_name = 'Bank Deposit'
        verbose_name_plural = 'Bank Deposits'
        ordering = ['-deposit_date']
        indexes = [
            models.Index(fields=['group', 'status']),
            models.Index(fields=['passenger', 'deposit_date']),
            models.Index(fields=['status', 'deposit_date']),
            models.Index(fields=['reference_number']),
        ]

    def __str__(self):
        return f"{self.group.code} - {self.amount} {self.currency} ({self.deposit_date})"

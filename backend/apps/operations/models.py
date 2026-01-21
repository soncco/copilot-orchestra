"""
Operations models: Hotel, Transportation, Accommodation, SpecialService, Staff, StaffAssignment.
"""
from django.db import models
from django.core.validators import MinValueValidator
from core.common.models import TimeStampedModel
from apps.circuits.models import Group
from apps.suppliers.models import Supplier
from apps.authentication.models import User


class Hotel(TimeStampedModel):
    """Hotel bookings for groups."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='hotels')
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name='hotel_bookings')

    # Hotel details
    hotel_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    # Dates
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    nights = models.IntegerField(validators=[MinValueValidator(1)])

    # Rooms
    room_type = models.CharField(max_length=100)
    number_of_rooms = models.IntegerField(validators=[MinValueValidator(1)])

    # Booking
    booking_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    # Pricing
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Details
    includes_breakfast = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'hotels'
        verbose_name = 'Hotel Booking'
        verbose_name_plural = 'Hotel Bookings'
        ordering = ['group', 'check_in_date']
        indexes = [
            models.Index(fields=['group', 'check_in_date']),
            models.Index(fields=['supplier', 'status']),
            models.Index(fields=['booking_reference']),
        ]

    def __str__(self):
        return f"{self.hotel_name} - {self.group.code}"

    def save(self, *args, **kwargs):
        """Calculate total price if not set."""
        if not self.total_price:
            self.total_price = self.price_per_night * self.nights * self.number_of_rooms
        super().save(*args, **kwargs)


class Transportation(TimeStampedModel):
    """Transportation bookings for groups."""

    TRANSPORT_TYPE_CHOICES = [
        ('bus', 'Bus'),
        ('van', 'Van'),
        ('car', 'Car'),
        ('train', 'Train'),
        ('boat', 'Boat'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='transportations')
    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, related_name='transport_bookings')

    # Transport details
    transport_type = models.CharField(
        max_length=20, choices=TRANSPORT_TYPE_CHOICES)
    vehicle_description = models.CharField(max_length=200, blank=True)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

    # Route
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    pickup_datetime = models.DateTimeField()
    dropoff_datetime = models.DateTimeField(null=True, blank=True)

    # Booking
    booking_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    # Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Driver info
    driver_name = models.CharField(max_length=200, blank=True)
    driver_phone = models.CharField(max_length=20, blank=True)

    # Details
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'transportation'
        verbose_name = 'Transportation'
        verbose_name_plural = 'Transportation'
        ordering = ['group', 'pickup_datetime']
        indexes = [
            models.Index(fields=['group', 'pickup_datetime']),
            models.Index(fields=['supplier', 'status']),
        ]

    def __str__(self):
        return f"{self.transport_type} - {self.origin} to {self.destination}"


class Accommodation(TimeStampedModel):
    """Room assignments for passengers."""

    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('twin', 'Twin'),
        ('triple', 'Triple'),
        ('suite', 'Suite'),
    ]

    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name='accommodations')

    # Room details
    room_number = models.CharField(max_length=20, blank=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)

    # Passengers (JSON array of passenger IDs)
    passengers = models.JSONField(
        default=list, help_text='Array of passenger IDs')

    # Special requests
    special_requests = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'accommodations'
        verbose_name = 'Accommodation'
        verbose_name_plural = 'Accommodations'
        ordering = ['hotel', 'room_number']
        indexes = [
            models.Index(fields=['hotel']),
        ]

    def __str__(self):
        return f"{self.hotel.hotel_name} - Room {self.room_number or 'TBA'}"


class SpecialService(TimeStampedModel):
    """Special services/activities for groups."""

    SERVICE_TYPE_CHOICES = [
        ('guide', 'Guide Service'),
        ('entrance', 'Entrance Fee'),
        ('activity', 'Activity'),
        ('meal', 'Meal'),
        ('show', 'Show/Event'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='special_services')
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='special_service_bookings',
        null=True,
        blank=True
    )

    # Service details
    service_type = models.CharField(
        max_length=20, choices=SERVICE_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Schedule
    service_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)

    # Booking
    booking_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_people = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    # Details
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'special_services'
        verbose_name = 'Special Service'
        verbose_name_plural = 'Special Services'
        ordering = ['group', 'service_date']
        indexes = [
            models.Index(fields=['group', 'service_date']),
            models.Index(fields=['service_type', 'status']),
        ]

    def __str__(self):
        return f"{self.name} - {self.group.code}"

    def save(self, *args, **kwargs):
        """Calculate total price if not set."""
        if not self.total_price:
            self.total_price = self.price_per_person * self.number_of_people
        super().save(*args, **kwargs)


class Staff(TimeStampedModel):
    """Staff members (guides, drivers, etc.)."""

    STAFF_TYPE_CHOICES = [
        ('guide', 'Tour Guide'),
        ('driver', 'Driver'),
        ('coordinator', 'Coordinator'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE_CHOICES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active')

    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)

    # Professional
    languages = models.JSONField(
        default=list, help_text='Array of language codes')
    certifications = models.TextField(blank=True)
    license_number = models.CharField(max_length=50, blank=True)

    # Payment
    rate_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='PEN')

    # Rating
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MinValueValidator(5)]
    )

    # Notes
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'staff'
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['staff_type', 'status']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_staff_type_display()})"

    @property
    def full_name(self):
        """Return staff member's full name."""
        return f"{self.first_name} {self.last_name}"


class StaffAssignment(TimeStampedModel):
    """Staff assignments to groups."""

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='staff_assignments')
    staff = models.ForeignKey(
        Staff, on_delete=models.PROTECT, related_name='assignments')

    # Assignment period
    start_date = models.DateField()
    end_date = models.DateField()

    # Role for this assignment
    role = models.CharField(
        max_length=100, help_text='e.g., Main Guide, Driver, etc.')

    # Payment
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='PEN')
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )

    # Notes
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'staff_assignments'
        verbose_name = 'Staff Assignment'
        verbose_name_plural = 'Staff Assignments'
        ordering = ['group', 'start_date']
        indexes = [
            models.Index(fields=['group', 'start_date']),
            models.Index(fields=['staff', 'start_date']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"{self.staff.full_name} - {self.group.code}"

    def save(self, *args, **kwargs):
        """Calculate total payment if not set."""
        if not self.total_payment:
            days = (self.end_date - self.start_date).days + 1
            self.total_payment = self.daily_rate * days
        super().save(*args, **kwargs)

"""
Circuit Management models: Programs, Groups, Passengers, Itineraries, Flights.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.common.models import TimeStampedModel
from apps.authentication.models import User


class Program(TimeStampedModel):
    """Tourism program/circuit definition."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_days = models.IntegerField(validators=[MinValueValidator(1)])
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Metadata
    max_passengers = models.IntegerField(validators=[MinValueValidator(1)], default=30)
    min_passengers = models.IntegerField(validators=[MinValueValidator(1)], default=10)
    
    class Meta:
        db_table = 'programs'
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Group(TimeStampedModel):
    """Group/Circuit instance."""
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    code = models.CharField(max_length=20, unique=True)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name='groups')
    name = models.CharField(max_length=200)
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Staff
    tour_conductor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conducted_groups',
        limit_choices_to={'role__in': ['tour_conductor', 'operations_manager', 'admin']}
    )
    
    # Status and capacity
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    current_passengers = models.IntegerField(default=0)
    max_passengers = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Financial
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'groups'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['program', 'start_date']),
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['tour_conductor']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def update_passenger_count(self):
        """Update current_passengers count."""
        self.current_passengers = self.passengers.filter(status='confirmed').count()
        self.save(update_fields=['current_passengers'])


class Passenger(TimeStampedModel):
    """Passenger in a group."""
    
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    DOCUMENT_TYPE_CHOICES = [
        ('dni', 'DNI'),
        ('passport', 'Passport'),
        ('ruc', 'RUC'),
        ('other', 'Other'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='passengers')
    
    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    document_number = models.CharField(max_length=50)
    nationality = models.CharField(max_length=3, default='PER')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')
    is_leader = models.BooleanField(default=False)
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Preferences
    special_requirements = models.TextField(blank=True)
    dietary_restrictions = models.TextField(blank=True)
    
    class Meta:
        db_table = 'passengers'
        verbose_name = 'Passenger'
        verbose_name_plural = 'Passengers'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['group', 'status']),
            models.Index(fields=['document_type', 'document_number']),
            models.Index(fields=['email']),
        ]
        unique_together = ['group', 'document_type', 'document_number']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        """Return passenger's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate passenger's age."""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class Itinerary(TimeStampedModel):
    """Daily itinerary for a group."""
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='itinerary_items')
    day_number = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateField()
    
    # Activities
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # Times
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    # Meals included
    breakfast_included = models.BooleanField(default=False)
    lunch_included = models.BooleanField(default=False)
    dinner_included = models.BooleanField(default=False)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'itinerary'
        verbose_name = 'Itinerary Item'
        verbose_name_plural = 'Itinerary'
        ordering = ['group', 'day_number']
        indexes = [
            models.Index(fields=['group', 'date']),
            models.Index(fields=['group', 'day_number']),
        ]
        unique_together = ['group', 'day_number']
    
    def __str__(self):
        return f"{self.group.code} - Day {self.day_number}: {self.title}"


class Flight(TimeStampedModel):
    """Flight information for a group."""
    
    FLIGHT_TYPE_CHOICES = [
        ('outbound', 'Outbound'),
        ('return', 'Return'),
        ('domestic', 'Domestic'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='flights')
    flight_type = models.CharField(max_length=20, choices=FLIGHT_TYPE_CHOICES)
    
    # Flight details
    airline = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    
    # Route
    departure_airport = models.CharField(max_length=100)
    departure_city = models.CharField(max_length=100)
    departure_country = models.CharField(max_length=3)
    arrival_airport = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    arrival_country = models.CharField(max_length=3)
    
    # Schedule
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    
    # Booking
    booking_reference = models.CharField(max_length=50, blank=True)
    booking_status = models.CharField(max_length=50, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'flights'
        verbose_name = 'Flight'
        verbose_name_plural = 'Flights'
        ordering = ['group', 'departure_datetime']
        indexes = [
            models.Index(fields=['group', 'flight_type']),
            models.Index(fields=['departure_datetime']),
            models.Index(fields=['booking_reference']),
        ]
    
    def __str__(self):
        return f"{self.flight_number} - {self.departure_city} to {self.arrival_city}"

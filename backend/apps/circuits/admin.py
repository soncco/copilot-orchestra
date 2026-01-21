"""
Admin configuration for circuits app.
"""
from django.contrib import admin
from .models import Program, Group, Passenger, Itinerary, Flight


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """Program admin configuration."""

    list_display = ['code', 'name', 'duration_days',
                    'base_price', 'currency', 'status']
    list_filter = ['status', 'currency']
    search_fields = ['code', 'name']
    ordering = ['code']


class PassengerInline(admin.TabularInline):
    """Inline passengers for group admin."""
    model = Passenger
    extra = 0
    fields = ['first_name', 'last_name',
              'document_number', 'status', 'total_price']
    readonly_fields = ['total_price']


class ItineraryInline(admin.TabularInline):
    """Inline itinerary for group admin."""
    model = Itinerary
    extra = 0
    fields = ['day_number', 'date', 'title', 'location']


class FlightInline(admin.TabularInline):
    """Inline flights for group admin."""
    model = Flight
    extra = 0
    fields = ['flight_type', 'airline', 'flight_number',
              'departure_city', 'arrival_city']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Group admin configuration."""

    list_display = [
        'code', 'name', 'program', 'start_date', 'end_date',
        'tour_conductor', 'status', 'current_passengers'
    ]
    list_filter = ['status', 'program']
    search_fields = ['code', 'name', 'program__name']
    ordering = ['-start_date']
    inlines = [PassengerInline, FlightInline, ItineraryInline]


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    """Passenger admin configuration."""

    list_display = [
        'full_name', 'group', 'document_number', 'nationality',
        'status', 'total_price'
    ]
    list_filter = ['status', 'nationality', 'gender']
    search_fields = ['first_name', 'last_name', 'email', 'document_number']
    ordering = ['group', 'last_name']


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    """Itinerary admin configuration."""

    list_display = ['group', 'day_number', 'date', 'title', 'location']
    list_filter = ['group']
    search_fields = ['title', 'location', 'description']
    ordering = ['group', 'day_number']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    """Flight admin configuration."""

    list_display = [
        'group', 'flight_type', 'airline', 'flight_number',
        'departure_city', 'arrival_city', 'departure_datetime'
    ]
    list_filter = ['flight_type', 'airline']
    search_fields = ['flight_number', 'booking_reference']
    ordering = ['group', 'departure_datetime']

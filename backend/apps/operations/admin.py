"""
Admin configuration for operations app.
"""
from django.contrib import admin
from .models import Hotel, Transportation, Accommodation, SpecialService, Staff, StaffAssignment


class AccommodationInline(admin.TabularInline):
    """Inline accommodations for hotel admin."""
    model = Accommodation
    extra = 0
    fields = ['room_number', 'room_type', 'passengers']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """Hotel booking admin configuration."""

    list_display = [
        'hotel_name', 'group', 'city', 'check_in_date',
        'check_out_date', 'nights', 'status', 'total_price'
    ]
    list_filter = ['status', 'city', 'includes_breakfast']
    search_fields = ['hotel_name', 'city', 'booking_reference', 'group__code']
    ordering = ['group', 'check_in_date']
    inlines = [AccommodationInline]


@admin.register(Transportation)
class TransportationAdmin(admin.ModelAdmin):
    """Transportation admin configuration."""

    list_display = [
        'group', 'transport_type', 'origin', 'destination',
        'pickup_datetime', 'status', 'total_price'
    ]
    list_filter = ['transport_type', 'status']
    search_fields = ['origin', 'destination', 'driver_name', 'group__code']
    ordering = ['group', 'pickup_datetime']


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    """Accommodation admin configuration."""

    list_display = ['hotel', 'room_number', 'room_type']
    list_filter = ['room_type']
    search_fields = ['hotel__hotel_name', 'room_number']
    ordering = ['hotel', 'room_number']


@admin.register(SpecialService)
class SpecialServiceAdmin(admin.ModelAdmin):
    """Special service admin configuration."""

    list_display = [
        'name', 'group', 'service_type', 'service_date',
        'status', 'total_price'
    ]
    list_filter = ['service_type', 'status']
    search_fields = ['name', 'description', 'location', 'group__code']
    ordering = ['group', 'service_date']


class StaffAssignmentInline(admin.TabularInline):
    """Inline assignments for staff admin."""
    model = StaffAssignment
    extra = 0
    fields = ['group', 'start_date', 'end_date',
              'role', 'daily_rate', 'payment_status']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """Staff admin configuration."""

    list_display = [
        'full_name', 'staff_type', 'status', 'phone',
        'rating', 'rate_per_day'
    ]
    list_filter = ['staff_type', 'status', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering = ['last_name', 'first_name']
    inlines = [StaffAssignmentInline]


@admin.register(StaffAssignment)
class StaffAssignmentAdmin(admin.ModelAdmin):
    """Staff assignment admin configuration."""

    list_display = [
        'staff', 'group', 'role', 'start_date', 'end_date',
        'total_payment', 'payment_status'
    ]
    list_filter = ['payment_status', 'role']
    search_fields = ['staff__first_name',
                     'staff__last_name', 'group__code', 'role']
    ordering = ['group', 'start_date']

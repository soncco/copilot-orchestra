"""
Serializers for operations app.
"""
from rest_framework import serializers
from .models import Hotel, Transportation, Accommodation, SpecialService, Staff, StaffAssignment


class HotelSerializer(serializers.ModelSerializer):
    """Hotel booking serializer."""

    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True)
    group_code = serializers.CharField(source='group.code', read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id', 'group', 'group_code', 'supplier', 'supplier_name',
            'hotel_name', 'city', 'address', 'check_in_date', 'check_out_date',
            'nights', 'room_type', 'number_of_rooms', 'booking_reference',
            'status', 'price_per_night', 'total_price', 'currency',
            'includes_breakfast', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate dates and calculate nights."""
        if 'check_in_date' in attrs and 'check_out_date' in attrs:
            if attrs['check_in_date'] >= attrs['check_out_date']:
                raise serializers.ValidationError({
                    'check_out_date': 'Check-out date must be after check-in date'
                })
            attrs['nights'] = (attrs['check_out_date'] -
                               attrs['check_in_date']).days
        return attrs


class TransportationSerializer(serializers.ModelSerializer):
    """Transportation booking serializer."""

    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True)
    group_code = serializers.CharField(source='group.code', read_only=True)

    class Meta:
        model = Transportation
        fields = [
            'id', 'group', 'group_code', 'supplier', 'supplier_name',
            'transport_type', 'vehicle_description', 'capacity',
            'origin', 'destination', 'pickup_datetime', 'dropoff_datetime',
            'booking_reference', 'status', 'total_price', 'currency',
            'driver_name', 'driver_phone', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AccommodationSerializer(serializers.ModelSerializer):
    """Accommodation assignment serializer."""

    hotel_name = serializers.CharField(
        source='hotel.hotel_name', read_only=True)

    class Meta:
        model = Accommodation
        fields = [
            'id', 'hotel', 'hotel_name', 'room_number', 'room_type',
            'passengers', 'special_requests', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SpecialServiceSerializer(serializers.ModelSerializer):
    """Special service serializer."""

    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True, allow_null=True)
    group_code = serializers.CharField(source='group.code', read_only=True)

    class Meta:
        model = SpecialService
        fields = [
            'id', 'group', 'group_code', 'supplier', 'supplier_name',
            'service_type', 'name', 'description', 'service_date',
            'start_time', 'end_time', 'location', 'booking_reference',
            'status', 'price_per_person', 'number_of_people',
            'total_price', 'currency', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StaffSerializer(serializers.ModelSerializer):
    """Staff member serializer."""

    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Staff
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'staff_type', 'status', 'email', 'phone', 'address', 'city',
            'languages', 'certifications', 'license_number',
            'rate_per_day', 'currency', 'rating', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StaffAssignmentSerializer(serializers.ModelSerializer):
    """Staff assignment serializer."""

    staff_name = serializers.CharField(
        source='staff.full_name', read_only=True)
    group_code = serializers.CharField(source='group.code', read_only=True)

    class Meta:
        model = StaffAssignment
        fields = [
            'id', 'group', 'group_code', 'staff', 'staff_name',
            'start_date', 'end_date', 'role', 'daily_rate',
            'total_payment', 'currency', 'payment_status', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate dates."""
        if 'start_date' in attrs and 'end_date' in attrs:
            if attrs['start_date'] > attrs['end_date']:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after or equal to start date'
                })
        return attrs

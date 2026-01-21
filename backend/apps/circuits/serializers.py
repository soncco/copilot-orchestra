"""
Serializers for circuits app.
"""
from rest_framework import serializers
from .models import Program, Group, Passenger, Itinerary, Flight
from apps.authentication.serializers import UserSerializer


class ProgramSerializer(serializers.ModelSerializer):
    """Program serializer."""

    groups_count = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            'id', 'code', 'name', 'description', 'duration_days',
            'base_price', 'currency', 'status', 'max_passengers',
            'min_passengers', 'groups_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_groups_count(self, obj):
        """Get count of groups using this program."""
        return obj.groups.count()


class FlightSerializer(serializers.ModelSerializer):
    """Flight serializer."""

    class Meta:
        model = Flight
        fields = [
            'id', 'group', 'flight_type', 'airline', 'flight_number',
            'departure_airport', 'departure_city', 'departure_country',
            'arrival_airport', 'arrival_city', 'arrival_country',
            'departure_datetime', 'arrival_datetime', 'booking_reference',
            'booking_status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ItinerarySerializer(serializers.ModelSerializer):
    """Itinerary serializer."""

    class Meta:
        model = Itinerary
        fields = [
            'id', 'group', 'day_number', 'date', 'title', 'description',
            'location', 'start_time', 'end_time', 'breakfast_included',
            'lunch_included', 'dinner_included', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PassengerSerializer(serializers.ModelSerializer):
    """Passenger serializer."""

    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()

    class Meta:
        model = Passenger
        fields = [
            'id', 'group', 'first_name', 'last_name', 'full_name',
            'document_type', 'document_number', 'nationality',
            'date_of_birth', 'age', 'gender', 'email', 'phone',
            'emergency_contact_name', 'emergency_contact_phone',
            'status', 'is_leader', 'base_price', 'additional_charges',
            'discount', 'total_price', 'currency', 'special_requirements',
            'dietary_restrictions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate passenger data."""
        # Calculate total price
        base_price = attrs.get('base_price', 0)
        additional = attrs.get('additional_charges', 0)
        discount = attrs.get('discount', 0)
        attrs['total_price'] = base_price + additional - discount

        return attrs


class PassengerCreateSerializer(serializers.ModelSerializer):
    """Passenger creation serializer."""

    class Meta:
        model = Passenger
        fields = [
            'group', 'first_name', 'last_name', 'document_type',
            'document_number', 'nationality', 'date_of_birth', 'gender',
            'email', 'phone', 'emergency_contact_name', 'emergency_contact_phone',
            'status', 'is_leader', 'base_price', 'additional_charges',
            'discount', 'special_requirements', 'dietary_restrictions'
        ]

    def validate(self, attrs):
        """Validate and calculate total price."""
        base_price = attrs.get('base_price', 0)
        additional = attrs.get('additional_charges', 0)
        discount = attrs.get('discount', 0)
        attrs['total_price'] = base_price + additional - discount

        # Get currency from group
        if 'group' in attrs:
            attrs['currency'] = attrs['group'].program.currency

        return attrs


class GroupListSerializer(serializers.ModelSerializer):
    """Group list serializer (lightweight)."""

    program_name = serializers.CharField(source='program.name', read_only=True)
    tour_conductor_name = serializers.CharField(
        source='tour_conductor.full_name', read_only=True)

    class Meta:
        model = Group
        fields = [
            'id', 'code', 'name', 'program', 'program_name',
            'start_date', 'end_date', 'tour_conductor',
            'tour_conductor_name', 'status', 'current_passengers',
            'max_passengers', 'total_cost', 'total_sales'
        ]
        read_only_fields = ['id', 'current_passengers']


class GroupDetailSerializer(serializers.ModelSerializer):
    """Group detail serializer (with related data)."""

    program = ProgramSerializer(read_only=True)
    program_id = serializers.UUIDField(write_only=True)
    tour_conductor = UserSerializer(read_only=True)
    tour_conductor_id = serializers.UUIDField(
        write_only=True, required=False, allow_null=True)

    passengers = PassengerSerializer(many=True, read_only=True)
    passengers_count = serializers.SerializerMethodField()

    flights = FlightSerializer(many=True, read_only=True)
    itinerary_items = ItinerarySerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            'id', 'code', 'name', 'program', 'program_id',
            'start_date', 'end_date', 'tour_conductor', 'tour_conductor_id',
            'status', 'current_passengers', 'max_passengers', 'passengers_count',
            'total_cost', 'total_sales', 'notes', 'passengers',
            'flights', 'itinerary_items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'current_passengers',
                            'created_at', 'updated_at']

    def get_passengers_count(self, obj):
        """Get passenger count by status."""
        return {
            'total': obj.passengers.count(),
            'confirmed': obj.passengers.filter(status='confirmed').count(),
            'reserved': obj.passengers.filter(status='reserved').count(),
            'cancelled': obj.passengers.filter(status='cancelled').count(),
        }


class GroupCreateSerializer(serializers.ModelSerializer):
    """Group creation serializer."""

    program_id = serializers.UUIDField()
    tour_conductor_id = serializers.UUIDField(required=False, allow_null=True)

    class Meta:
        model = Group
        fields = [
            'code', 'name', 'program_id', 'start_date', 'end_date',
            'tour_conductor_id', 'status', 'max_passengers', 'notes'
        ]

    def validate_program_id(self, value):
        """Validate program exists."""
        if not Program.objects.filter(id=value).exists():
            raise serializers.ValidationError('Program does not exist')
        return value

    def create(self, validated_data):
        """Create group."""
        program_id = validated_data.pop('program_id')
        tour_conductor_id = validated_data.pop('tour_conductor_id', None)

        validated_data['program_id'] = program_id
        if tour_conductor_id:
            validated_data['tour_conductor_id'] = tour_conductor_id

        return super().create(validated_data)


class ImportPassengersSerializer(serializers.Serializer):
    """Serializer for importing passengers from CSV/Excel."""

    file = serializers.FileField(required=True)
    group_id = serializers.UUIDField(required=True)

    def validate_file(self, value):
        """Validate file type."""
        allowed_extensions = ['csv', 'xlsx', 'xls']
        ext = value.name.split('.')[-1].lower()

        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                f'File type not supported. Allowed: {", ".join(allowed_extensions)}'
            )

        return value

    def validate_group_id(self, value):
        """Validate group exists."""
        if not Group.objects.filter(id=value).exists():
            raise serializers.ValidationError('Group does not exist')
        return value

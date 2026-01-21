"""
Views for circuits app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Program, Group, Passenger, Itinerary, Flight
from .serializers import (
    ProgramSerializer, GroupListSerializer, GroupDetailSerializer,
    GroupCreateSerializer, PassengerSerializer, PassengerCreateSerializer,
    ItinerarySerializer, FlightSerializer, ImportPassengersSerializer
)
from core.common.permissions import IsAdmin, IsOperationsManager
from core.common.pagination import StandardPagination


class ProgramViewSet(viewsets.ModelViewSet):
    """Program CRUD endpoints."""
    
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'currency']
    search_fields = ['code', 'name', 'description']
    ordering_fields = ['code', 'name', 'created_at', 'base_price']
    ordering = ['code']
    
    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        """Get all groups for a program."""
        program = self.get_object()
        groups = program.groups.all()
        
        page = self.paginate_queryset(groups)
        if page is not None:
            serializer = GroupListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = GroupListSerializer(groups, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """Group CRUD endpoints."""
    
    queryset = Group.objects.select_related('program', 'tour_conductor').all()
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['program', 'status', 'tour_conductor']
    search_fields = ['code', 'name', 'program__name']
    ordering_fields = ['code', 'start_date', 'created_at']
    ordering = ['-start_date']
    
    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'create':
            return GroupCreateSerializer
        elif self.action in ['retrieve']:
            return GroupDetailSerializer
        return GroupListSerializer
    
    @action(detail=True, methods=['get'])
    def passengers(self, request, pk=None):
        """Get all passengers for a group."""
        group = self.get_object()
        passengers = group.passengers.all()
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            passengers = passengers.filter(status=status_filter)
        
        page = self.paginate_queryset(passengers)
        if page is not None:
            serializer = PassengerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PassengerSerializer(passengers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def itinerary(self, request, pk=None):
        """Get itinerary for a group."""
        group = self.get_object()
        itinerary = group.itinerary_items.all()
        serializer = ItinerarySerializer(itinerary, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def flights(self, request, pk=None):
        """Get flights for a group."""
        group = self.get_object()
        flights = group.flights.all()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update group status."""
        group = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_status not in dict(Group.STATUS_CHOICES).keys():
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        group.status = new_status
        group.save(update_fields=['status', 'updated_at'])
        
        serializer = self.get_serializer(group)
        return Response(serializer.data)


class PassengerViewSet(viewsets.ModelViewSet):
    """Passenger CRUD endpoints."""
    
    queryset = Passenger.objects.select_related('group').all()
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['group', 'status', 'nationality']
    search_fields = ['first_name', 'last_name', 'email', 'document_number']
    ordering_fields = ['last_name', 'created_at']
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'create':
            return PassengerCreateSerializer
        return PassengerSerializer
    
    def perform_create(self, serializer):
        """Create passenger and update group count."""
        passenger = serializer.save()
        passenger.group.update_passenger_count()
    
    def perform_update(self, serializer):
        """Update passenger and update group count if status changed."""
        old_status = self.get_object().status
        passenger = serializer.save()
        
        if old_status != passenger.status:
            passenger.group.update_passenger_count()
    
    def perform_destroy(self, instance):
        """Delete passenger and update group count."""
        group = instance.group
        super().perform_destroy(instance)
        group.update_passenger_count()
    
    @action(detail=False, methods=['post'])
    def import_passengers(self, request):
        """Import passengers from CSV/Excel file."""
        serializer = ImportPassengersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # TODO: Implement CSV/Excel import logic
        # This would parse the file and create passenger records
        
        return Response({
            'message': 'Import feature coming soon',
            'file': serializer.validated_data['file'].name,
            'group_id': serializer.validated_data['group_id']
        })
    
    @action(detail=False, methods=['get'])
    def export_passengers(self, request):
        """Export passengers to CSV."""
        group_id = request.query_params.get('group')
        
        if not group_id:
            return Response(
                {'error': 'Group ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Implement CSV export logic
        # This would generate a CSV file with passenger data
        
        return Response({
            'message': 'Export feature coming soon',
            'group_id': group_id
        })


class ItineraryViewSet(viewsets.ModelViewSet):
    """Itinerary CRUD endpoints."""
    
    queryset = Itinerary.objects.select_related('group').all()
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['group']
    ordering_fields = ['day_number', 'date']
    ordering = ['group', 'day_number']


class FlightViewSet(viewsets.ModelViewSet):
    """Flight CRUD endpoints."""
    
    queryset = Flight.objects.select_related('group').all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['group', 'flight_type']
    ordering_fields = ['departure_datetime']
    ordering = ['group', 'departure_datetime']

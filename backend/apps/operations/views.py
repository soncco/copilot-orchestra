"""
Views for operations app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Hotel, Transportation, Accommodation, SpecialService, Staff, StaffAssignment
from .serializers import (
    HotelSerializer, TransportationSerializer, AccommodationSerializer,
    SpecialServiceSerializer, StaffSerializer, StaffAssignmentSerializer
)
from core.common.permissions import IsOperationsManager
from core.common.pagination import StandardPagination


class HotelViewSet(viewsets.ModelViewSet):
    """Hotel booking CRUD endpoints."""

    queryset = Hotel.objects.select_related('group', 'supplier').all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['group', 'supplier', 'status', 'city']
    search_fields = ['hotel_name', 'city', 'booking_reference']
    ordering_fields = ['check_in_date', 'total_price']
    ordering = ['group', 'check_in_date']


class TransportationViewSet(viewsets.ModelViewSet):
    """Transportation booking CRUD endpoints."""

    queryset = Transportation.objects.select_related('group', 'supplier').all()
    serializer_class = TransportationSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['group', 'supplier', 'transport_type', 'status']
    search_fields = ['origin', 'destination',
                     'driver_name', 'booking_reference']
    ordering_fields = ['pickup_datetime', 'total_price']
    ordering = ['group', 'pickup_datetime']


class AccommodationViewSet(viewsets.ModelViewSet):
    """Accommodation assignment CRUD endpoints."""

    queryset = Accommodation.objects.select_related('hotel').all()
    serializer_class = AccommodationSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['hotel', 'room_type']
    ordering_fields = ['room_number']
    ordering = ['hotel', 'room_number']


class SpecialServiceViewSet(viewsets.ModelViewSet):
    """Special service CRUD endpoints."""

    queryset = SpecialService.objects.select_related('group', 'supplier').all()
    serializer_class = SpecialServiceSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['group', 'supplier', 'service_type', 'status']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['service_date', 'total_price']
    ordering = ['group', 'service_date']


class StaffViewSet(viewsets.ModelViewSet):
    """Staff member CRUD endpoints."""

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['staff_type', 'status', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['last_name', 'rating', 'rate_per_day']
    ordering = ['last_name', 'first_name']

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """Get all assignments for a staff member."""
        staff = self.get_object()
        assignments = staff.assignments.all()

        page = self.paginate_queryset(assignments)
        if page is not None:
            serializer = StaffAssignmentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StaffAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)


class StaffAssignmentViewSet(viewsets.ModelViewSet):
    """Staff assignment CRUD endpoints."""

    queryset = StaffAssignment.objects.select_related('group', 'staff').all()
    serializer_class = StaffAssignmentSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['group', 'staff', 'payment_status']
    ordering_fields = ['start_date', 'total_payment']
    ordering = ['group', 'start_date']

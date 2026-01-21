"""
Views for suppliers app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import date

from .models import Supplier, SupplierService, PricePeriod, ExchangeRate
from .serializers import (
    SupplierSerializer, SupplierServiceSerializer,
    SupplierServiceCreateSerializer, PricePeriodSerializer,
    ExchangeRateSerializer, ConvertCurrencySerializer
)
from core.common.permissions import IsOperationsManager
from core.common.pagination import StandardPagination


class SupplierViewSet(viewsets.ModelViewSet):
    """Supplier CRUD endpoints."""

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['supplier_type', 'status', 'country', 'city']
    search_fields = ['code', 'name', 'contact_name', 'email', 'tax_id']
    ordering_fields = ['code', 'name', 'rating', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        """Get all services for a supplier."""
        supplier = self.get_object()
        services = supplier.services.all()

        # Filter by active status
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            services = services.filter(is_active=is_active.lower() == 'true')

        page = self.paginate_queryset(services)
        if page is not None:
            serializer = SupplierServiceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SupplierServiceSerializer(services, many=True)
        return Response(serializer.data)


class SupplierServiceViewSet(viewsets.ModelViewSet):
    """Supplier service CRUD endpoints."""

    queryset = SupplierService.objects.select_related('supplier').all()
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['supplier', 'service_type', 'is_active', 'currency']
    search_fields = ['name', 'description', 'supplier__name']
    ordering_fields = ['name', 'base_price', 'created_at']
    ordering = ['supplier', 'name']

    def get_serializer_class(self):
        """Return appropriate serializer."""
        if self.action == 'create':
            return SupplierServiceCreateSerializer
        return SupplierServiceSerializer

    @action(detail=True, methods=['get'])
    def price_periods(self, request, pk=None):
        """Get price periods for a service."""
        service = self.get_object()
        periods = service.price_periods.all()
        serializer = PricePeriodSerializer(periods, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def price_for_date(self, request, pk=None):
        """Get price for a specific date."""
        service = self.get_object()
        date_str = request.query_params.get('date')

        if not date_str:
            return Response(
                {'error': 'Date parameter is required (YYYY-MM-DD)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            query_date = date.fromisoformat(date_str)
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find applicable price period
        period = service.price_periods.filter(
            start_date__lte=query_date,
            end_date__gte=query_date
        ).first()

        if period:
            return Response({
                'date': query_date,
                'price': period.price,
                'currency': period.currency,
                'season': period.season,
                'period': PricePeriodSerializer(period).data
            })
        else:
            return Response({
                'date': query_date,
                'price': service.base_price,
                'currency': service.currency,
                'season': 'base',
                'period': None
            })


class PricePeriodViewSet(viewsets.ModelViewSet):
    """Price period CRUD endpoints."""

    queryset = PricePeriod.objects.select_related('service').all()
    serializer_class = PricePeriodSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['service', 'season']
    ordering_fields = ['start_date', 'price']
    ordering = ['service', 'start_date']


class ExchangeRateViewSet(viewsets.ModelViewSet):
    """Exchange rate CRUD endpoints."""

    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated, IsOperationsManager]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['from_currency', 'to_currency', 'date']
    ordering_fields = ['date', 'from_currency']
    ordering = ['-date', 'from_currency']

    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest exchange rates for a currency pair."""
        from_currency = request.query_params.get('from')
        to_currency = request.query_params.get('to')

        if not from_currency or not to_currency:
            return Response(
                {'error': 'Both "from" and "to" currency parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rate = ExchangeRate.objects.filter(
            from_currency=from_currency.upper(),
            to_currency=to_currency.upper()
        ).first()

        if not rate:
            return Response(
                {'error': f'No exchange rate found for {from_currency}/{to_currency}'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(rate)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def convert(self, request):
        """Convert amount from one currency to another."""
        serializer = ConvertCurrencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        from_currency = serializer.validated_data['from_currency'].upper()
        to_currency = serializer.validated_data['to_currency'].upper()
        query_date = serializer.validated_data.get('date', date.today())

        if from_currency == to_currency:
            return Response({
                'amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
                'converted_amount': amount,
                'rate': 1,
                'date': query_date
            })

        # Find exchange rate for the date
        rate_obj = ExchangeRate.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency,
            date__lte=query_date
        ).first()

        if not rate_obj:
            return Response(
                {'error': f'No exchange rate found for {from_currency}/{to_currency} on {query_date}'},
                status=status.HTTP_404_NOT_FOUND
            )

        converted_amount = amount * rate_obj.rate

        return Response({
            'amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'converted_amount': round(converted_amount, 2),
            'rate': rate_obj.rate,
            'date': rate_obj.date
        })

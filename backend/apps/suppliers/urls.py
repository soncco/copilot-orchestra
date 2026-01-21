"""
URL configuration for suppliers app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SupplierViewSet, SupplierServiceViewSet,
    PricePeriodViewSet, ExchangeRateViewSet
)

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'services', SupplierServiceViewSet, basename='services')
router.register(r'price-periods', PricePeriodViewSet, basename='price-periods')
router.register(r'exchange-rates', ExchangeRateViewSet,
                basename='exchange-rates')

urlpatterns = router.urls

"""
Financial URL configuration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GroupCostViewSet,
    AdditionalSaleViewSet,
    CommissionViewSet,
    InvoiceViewSet,
    BankDepositViewSet
)

router = DefaultRouter()
router.register(r'group-costs', GroupCostViewSet, basename='groupcost')
router.register(r'additional-sales', AdditionalSaleViewSet,
                basename='additionalsale')
router.register(r'commissions', CommissionViewSet, basename='commission')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'bank-deposits', BankDepositViewSet, basename='bankdeposit')

urlpatterns = [
    path('', include(router.urls)),
]

"""
URL configuration for operations app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HotelViewSet, TransportationViewSet, AccommodationViewSet,
    SpecialServiceViewSet, StaffViewSet, StaffAssignmentViewSet
)

router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotels')
router.register(r'transportation', TransportationViewSet,
                basename='transportation')
router.register(r'accommodations', AccommodationViewSet,
                basename='accommodations')
router.register(r'special-services', SpecialServiceViewSet,
                basename='special-services')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'staff-assignments', StaffAssignmentViewSet,
                basename='staff-assignments')

urlpatterns = router.urls

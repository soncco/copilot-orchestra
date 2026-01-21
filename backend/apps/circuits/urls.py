"""
URL configuration for circuits app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProgramViewSet, GroupViewSet, PassengerViewSet,
    ItineraryViewSet, FlightViewSet
)

router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='programs')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'passengers', PassengerViewSet, basename='passengers')
router.register(r'itinerary', ItineraryViewSet, basename='itinerary')
router.register(r'flights', FlightViewSet, basename='flights')

urlpatterns = router.urls

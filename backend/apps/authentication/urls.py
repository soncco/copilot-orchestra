"""
Authentication URL configuration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='users')
router.register(r'audit', AuditLogViewSet, basename='audit')

urlpatterns = router.urls

"""
Custom permissions for role-based access control.
"""
from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    """User must be authenticated."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAdmin(permissions.BasePermission):
    """Only admin users can access."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsOperationsManager(permissions.BasePermission):
    """Admin or Operations Manager can access."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
            request.user.role in ['admin', 'operations_manager']


class IsTourConductor(permissions.BasePermission):
    """Admin, Operations Manager, or Tour Conductor can access."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
            request.user.role in [
                'admin', 'operations_manager', 'tour_conductor']


class IsAccountant(permissions.BasePermission):
    """Admin or Accountant can access."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
            request.user.role in ['admin', 'accountant']


class IsFinanceManager(permissions.BasePermission):
    """Admin or Finance Manager can access."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
            request.user.role in ['admin', 'accountant', 'operations_manager']


class IsViewer(permissions.BasePermission):
    """All authenticated users can access (read-only)."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """Object owner or admin can access."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True

        # Check if object has user field
        if hasattr(obj, 'user'):
            return obj.user == request.user

        # Check if object has created_by field
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user

        return False

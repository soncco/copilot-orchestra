"""
Custom exception handlers and error classes.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError


class BaseAPIException(Exception):
    """Base exception for API errors."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'
    default_message = 'An error occurred'

    def __init__(self, message=None, code=None, status_code=None):
        self.message = message or self.default_message
        self.code = code or self.default_code
        if status_code:
            self.status_code = status_code


class ValidationError(BaseAPIException):
    """Validation error exception."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'validation_error'
    default_message = 'Validation failed'


class NotFoundError(BaseAPIException):
    """Resource not found exception."""
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'not_found'
    default_message = 'Resource not found'


class ConflictError(BaseAPIException):
    """Conflict error (e.g., duplicate resource)."""
    status_code = status.HTTP_409_CONFLICT
    default_code = 'conflict'
    default_message = 'Resource already exists'


class UnauthorizedError(BaseAPIException):
    """Unauthorized access exception."""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'unauthorized'
    default_message = 'Authentication required'


class ForbiddenError(BaseAPIException):
    """Forbidden access exception."""
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'forbidden'
    default_message = 'Permission denied'


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    Handles both DRF exceptions and our custom exceptions.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Handle custom exceptions
    if isinstance(exc, BaseAPIException):
        return Response(
            {
                'error': {
                    'code': exc.code,
                    'message': exc.message
                }
            },
            status=exc.status_code
        )

    # Handle Django validation errors
    if isinstance(exc, DjangoValidationError):
        return Response(
            {
                'error': {
                    'code': 'validation_error',
                    'message': str(exc)
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # If response is already handled by DRF
    if response is not None:
        # Format error response consistently
        if isinstance(response.data, dict):
            response.data = {
                'error': {
                    'code': getattr(exc, 'default_code', 'error'),
                    'message': response.data.get('detail', str(exc))
                }
            }

    return response

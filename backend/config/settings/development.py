"""
Development settings.
"""
from .base import *

DEBUG = True

# Additional development apps
INSTALLED_APPS += [
    'django_extensions',
]

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# Console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django Debug Toolbar (optional)
if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS += ['debug_toolbar']
        MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
        INTERNAL_IPS = ['127.0.0.1', 'localhost']
    except ImportError:
        pass

# CORS - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

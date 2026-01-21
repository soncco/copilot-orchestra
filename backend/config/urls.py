"""
URL Configuration for TravesIA project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/circuits/', include('apps.circuits.urls')),
    path('api/v1/suppliers/', include('apps.suppliers.urls')),
    path('api/v1/operations/', include('apps.operations.urls')),
    path('api/v1/financial/', include('apps.financial.urls')),
    path('api/v1/documents/', include('apps.documents.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

# Customize admin
admin.site.site_header = "TravesIA Admin"
admin.site.site_title = "TravesIA"
admin.site.index_title = "Panel de Administración"

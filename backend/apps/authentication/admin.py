"""
Authentication admin configuration.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserSession, AuditLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User admin configuration."""

    list_display = ['email', 'first_name', 'last_name',
                    'role', 'is_active', 'mfa_enabled']
    list_filter = ['role', 'is_active', 'mfa_enabled', 'email_verified']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
         'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        ('Permissions', {
         'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('MFA', {'fields': ('mfa_enabled', 'mfa_secret')}),
        ('Metadata', {'fields': ('email_verified',
         'email_verified_at', 'last_login', 'last_login_ip')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """User session admin configuration."""

    list_display = ['user', 'ip_address',
                    'created_at', 'expires_at', 'last_activity']
    list_filter = ['created_at', 'expires_at']
    search_fields = ['user__email', 'ip_address']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Audit log admin configuration."""

    list_display = ['user', 'action',
                    'resource_type', 'resource_id', 'created_at']
    list_filter = ['action', 'resource_type', 'created_at']
    search_fields = ['user__email', 'resource_type',
                     'resource_id', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

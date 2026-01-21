"""
User and authentication models.
"""
import uuid
import pyotp
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from core.common.models import TimeStampedModel


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Custom user model."""

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('operations_manager', 'Operations Manager'),
        ('tour_conductor', 'Tour Conductor'),
        ('accountant', 'Accountant'),
        ('viewer', 'Viewer'),
    ]

    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=30, choices=ROLE_CHOICES, default='viewer')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # MFA
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=32, blank=True, null=True)

    # Profile
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Metadata
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}"

    def enable_mfa(self):
        """Enable MFA for user and generate secret."""
        if not self.mfa_secret:
            self.mfa_secret = pyotp.random_base32()
        self.mfa_enabled = True
        self.save()
        return self.get_mfa_uri()

    def disable_mfa(self):
        """Disable MFA for user."""
        self.mfa_enabled = False
        self.save()

    def get_mfa_uri(self):
        """Get MFA provisioning URI for QR code."""
        if not self.mfa_secret:
            return None
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.provisioning_uri(
            name=self.email,
            issuer_name='TravesIA'
        )

    def verify_mfa_token(self, token):
        """Verify MFA token."""
        if not self.mfa_enabled or not self.mfa_secret:
            return False
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.verify(token, valid_window=1)


class UserSession(TimeStampedModel):
    """Active user sessions."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sessions')
    token = models.CharField(max_length=500)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, blank=True)
    expires_at = models.DateTimeField()
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_sessions'
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        indexes = [
            models.Index(fields=['user', 'expires_at']),
            models.Index(fields=['token']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.ip_address}"

    def is_expired(self):
        """Check if session is expired."""
        return timezone.now() > self.expires_at


class AuditLog(models.Model):
    """Audit log for tracking user actions."""

    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('export', 'Export'),
        ('import', 'Import'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_log'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['action', 'created_at']),
            models.Index(fields=['resource_type', 'resource_id']),
        ]

    def __str__(self):
        return f"{self.user.email if self.user else 'System'} - {self.action} - {self.resource_type}"

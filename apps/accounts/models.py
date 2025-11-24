from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import uuid

class User_Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name

class UsersManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('status', True)
        # Assuming role_id 1 is Admin. We might need to create it first or handle it.
        # For now, we'll just set it if provided or handle in signal/migration.
        # But since role_id is a ForeignKey, it must exist.
        # We will handle this by creating a default role if not exists in a migration or signal.
        # For superuser creation via command line, we might need a workaround or custom command.
        return self.create_user(email, password, **extra_fields)

class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(User_Roles, on_delete=models.SET_NULL, null=True, db_column='role_id')
    email = models.EmailField(unique=True, max_length=255, db_index=True)
    status = models.BooleanField(default=True, db_index=True)
    
    # Email Verification Fields
    email_verified = models.BooleanField(default=False, db_index=True)
    verification_token = models.CharField(max_length=6, null=True, blank=True)
    verification_token_created = models.DateTimeField(null=True, blank=True)
    
    # Password Reset Fields
    reset_token = models.UUIDField(null=True, blank=True)
    reset_token_created = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        # Simplified for now, can be based on role
        return True

    @property
    def is_admin(self):
        return True
    
    @property
    def is_active(self):
        """Override is_active to check both status and email verification"""
        return self.status and self.email_verified
    
    def generate_verification_token(self):
        """Generate a 6-digit OTP for email verification"""
        import random
        self.verification_token = str(random.randint(100000, 999999))
        self.verification_token_created = timezone.now()
        self.save()
        return self.verification_token
    
    def verify_otp(self, otp):
        """Verify OTP and check expiration (1 minute)"""
        if not self.verification_token or not self.verification_token_created:
            return False
        
        # Check if OTP matches
        if self.verification_token != otp:
            return False
        
        # Check if OTP is expired (1 minute)
        expiration_time = self.verification_token_created + timezone.timedelta(minutes=1)
        if timezone.now() > expiration_time:
            return False
        
        # Mark email as verified
        self.email_verified = True
        self.verification_token = None
        self.verification_token_created = None
        self.save()
        return True
    
    def generate_reset_token(self):
        """Generate UUID token for password reset"""
        self.reset_token = uuid.uuid4()
        self.reset_token_created = timezone.now()
        self.save()
        return self.reset_token
    
    def verify_reset_token(self, token):
        """Verify reset token and check expiration (1 hour)"""
        if not self.reset_token or not self.reset_token_created:
            return False
        
        # Check if token matches
        if str(self.reset_token) != str(token):
            return False
        
        # Check if token is expired (1 hour)
        expiration_time = self.reset_token_created + timezone.timedelta(hours=1)
        if timezone.now() > expiration_time:
            return False
        
        return True


class LoginAttempt(models.Model):
    """Track login attempts for security"""
    email = models.EmailField(max_length=255, db_index=True)
    ip_address = models.GenericIPAddressField()
    attempted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    successful = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'login_attempts'
        indexes = [
            models.Index(fields=['email', 'attempted_at']),
            models.Index(fields=['ip_address', 'attempted_at']),
        ]
    
    @staticmethod
    def is_locked(email, ip_address):
        """Check if account is locked due to failed attempts"""
        # Get failed attempts in last 15 minutes
        fifteen_minutes_ago = timezone.now() - timezone.timedelta(minutes=15)
        failed_attempts = LoginAttempt.objects.filter(
            email=email,
            ip_address=ip_address,
            successful=False,
            attempted_at__gte=fifteen_minutes_ago
        ).count()
        
        return failed_attempts >= 5
    
    @staticmethod
    def record_attempt(email, ip_address, successful=False):
        """Record a login attempt"""
        LoginAttempt.objects.create(
            email=email,
            ip_address=ip_address,
            successful=successful
        )
    
    @staticmethod
    def clear_attempts(email, ip_address):
        """Clear failed attempts after successful login"""
        LoginAttempt.objects.filter(
            email=email,
            ip_address=ip_address,
            successful=False
        ).delete()

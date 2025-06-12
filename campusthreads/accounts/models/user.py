from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import timedelta, datetime, timezone
from rest_framework_simplejwt.tokens import AccessToken

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'teacher'),
        ('admin', 'Admin'),
    ]
    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('deleted', 'Deleted'),    
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    profile_picture = models.URLField(blank=True, default='')
    bio = models.TextField(blank=True, default='')
    last_login = models.DateTimeField(null=True, blank=True)
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='active')
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_token_expires = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_email_verification_token(self):
        exp = datetime.now(timezone.utc) + timedelta(minutes=30)
        token = AccessToken()
        token['user_id'] = self.pk
        token.set_exp(from_time=datetime.now(timezone.utc), lifetime=timedelta(hours=24))
        token_str = str(token)
        self.email_verification_token = token_str
        self.email_verification_token_expires = exp
        self.save(update_fields=["email_verification_token","email_verification_token_expires"])
        return token_str


    def verify_email_token(self, token):
        from rest_framework_simplejwt.exceptions import TokenError
        from rest_framework_simplejwt.tokens import UntypedToken
        
        try:
            payload = UntypedToken(token)
            if(
                token == self.email_verification_token and
                self.email_verification_token_expires and
                self.email_verification_token_expires > datetime.now(timezone.utc)
            ):
                self.email_verified = True
                self.email_verification_token = None
                self.email_verification_token_expires = None
                self.save(update_fields=["email_verified", "email_verification_token", "email_verification_token_expires"])
                return True
        except TokenError:
            return False
        return False
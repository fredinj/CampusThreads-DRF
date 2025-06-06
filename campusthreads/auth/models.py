from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta
import jwt

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_email_verification_token(self):
        exp = datetime.now(datetime.timezone.utc) + timedelta(hours=24)
        token = jwt.encode(
            {"user_id": self.pk, "exp":exp},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        self.email_verification_token = token
        self.email_verification_token_expires = exp
        self.save(update_fields=["email_verification_token","email_verification_token_expires"])
        return token

    def verify_email_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if(
                token == self.email_verification_token and
                self.email_verification_token_expires and
                self.email_verification_token_expires > datetime.now(datetime.timezone.utc)
            ):
                self.email_verified = True
                self.email_verification_token = None
                self.email_verification_token_expires = None
                self.save(updated_fields=["email_verified", "email_verification_token", "email_verification_token_expires"])
                return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        return False
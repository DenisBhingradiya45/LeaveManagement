from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

ROLE_CHOICES = (
    ("Student", "Student"),
    ("Faculty", "Faculty"),
)

WORK_CHOICES = (
    ("Online", "Online"),
    ("On-Campus", "On-Campus"),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    work_mode = models.CharField(max_length=50, choices=WORK_CHOICES)
    status = models.CharField(max_length=12, default='pending')
    is_approved = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    ceated_at = models.DateTimeField(auto_now_add=True)

class ForgotPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
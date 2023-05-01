from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


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
    ROLE_CHOICES = (
        ("Student", "Student"),
        ("Faculty", "Faculty"),
    )
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
    WORK_CHOICES = (
        ("Online", "Online"),
        ("On-Campus", "On-Campus"),
    )
    STATUS_CHOICES = (
        ("Approved ", "Approved"),
        ("Denied", "Denied"),
        ("Pending", "Pending"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    work_mode = models.CharField(max_length=50, choices=WORK_CHOICES)
    status = models.CharField(choices=STATUS_CHOICES, max_length=9, default='Pending')
    is_approved = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    ceated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ceated_at']


class ForgotPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

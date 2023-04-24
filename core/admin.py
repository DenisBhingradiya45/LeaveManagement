from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'role']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'work_mode', 'is_approved', 'start_date', 'end_date']
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('SignUp/', SignUp, name='SignUp'),
    path('SignIn/', SignIn, name='SignIn'),
    path('RequestLeave/', RequestLeave, name='RequestLeave'),
    path('DashBoard/', DashBoard, name='DashBoard'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
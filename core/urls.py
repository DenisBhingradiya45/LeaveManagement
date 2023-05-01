from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('SignUp/', SignUp, name='SignUp'),
    path('SignIn/', SignIn, name='SignIn'),
    path('LogOut/', LogOut, name='LogOut'),
    path('RequestLeave/', RequestLeave, name='RequestLeave'),
    path('DashBoard/', DashBoard, name='DashBoard'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('otp_verification/<str:email>/', otp_verification, name='otp_verification'),
    path('reset_password/<str:email>/', reset_password, name='reset_password'),
    path('approve_leave_request/<int:id>/', approve_leave_request, name='approve_leave_request'),
    path('deny_leave_request/<int:id>/', deny_leave_request, name='deny_leave_request'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


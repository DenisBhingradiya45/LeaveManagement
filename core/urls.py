from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('SignUp/', SignUp, name='SignUp'),
    path('SignIn/', SignIn, name='SignIn'),
    path('RequestLeave/', RequestLeave, name='RequestLeave'),
    path('DashBoard/', DashBoard, name='DashBoard'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/' ,auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset /<uidb64>/<token>/' ,auth_views .PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/' ,auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


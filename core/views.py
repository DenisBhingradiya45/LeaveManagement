from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
import random
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.cache import cache

# Create your views here.

def SignUp(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = CustomUserCreationForm(request.POST)
            if fm.is_valid():
                messages.success(request, 'Account Created Successfully !!')
                fm.save()
                return redirect('/DashBoard/')
        else:
            fm = CustomUserCreationForm()
        return render(request, 'SignUp.html', {'form': fm})
    else:
        return redirect('/DashBoard/')


def SignIn(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data = request.POST)
            if fm.is_valid():
                uemail = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(email = uemail, password = upass)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/DashBoard/')
                else:
                    messages.info(request, 'Try again! username or password is incorrect')
        else:
            fm = AuthenticationForm()
        return render(request, "SignIn.html", {"form":fm})
    else:
        return HttpResponseRedirect('/DashBoard/')

def LogOut(request):
    logout(request)
    return HttpResponseRedirect('/SignIn/')

def RequestLeave(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['reason']
            start_date = request.POST['start-date']
            end_date = request.POST['end-date']
            work_mode = request.POST['work-mode']
            user = request.user
            leave = Application.objects.create(
                user=user,
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                work_mode = work_mode
            )
            return redirect('/DashBoard/')
        return render(request, 'RequestLeave.html')
    else:
        return redirect('/SignIn/')
    
def DashBoard(request):
    if request.user.is_authenticated:
    #     fm = Application.objects.get(user=request.user)
        return render(request, 'DashBoard.html')
    else:
        return redirect('/SignIn/')


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = random.randint(100000, 999999)
                forgot_password = ForgotPassword.objects.create(user=user, otp=otp)
                forgot_password.save()
                subject = 'Your OTP for password reset'
                message = f'Your OTP is {otp}. Please use this to reset your password.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail(subject, message, email_from, recipient_list)
                return redirect('otp_verification', email=email)
            except User.DoesNotExist:
                invalid_email = True
                invalid_form = True
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = ForgotPasswordForm()
        invalid_email = False
        invalid_form = False

    context = {'form': form, 'invalid_form': invalid_form, 'invalid_email': invalid_email}
    return render(request, 'forgot_password.html', context)

def otp_verification(request, email):
    try:
        forgot_password = ForgotPassword.objects.filter(user__email=email).latest('timestamp')
        if request.method == 'POST':
            form = OTPVerificationForm(request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                if otp == forgot_password.otp:
                    return redirect('reset_password', email=email)
                else:
                    form.add_error('otp', 'Incorrect OTP. Please try again.')
        else:
            form = OTPVerificationForm(initial={'email': email})
        context = {'form': form}
        return render(request, 'otp_verification.html', context)
    except ForgotPassword.DoesNotExist:
        return redirect('forgot_password')

def reset_password(request, email):
    try:
        forgot_password = ForgotPassword.objects.filter(user__email=email).latest('timestamp')
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']
                if password == confirm_password:
                    user = forgot_password.user
                    user.set_password(password)
                    user.save()
                    forgot_password.delete()
                    messages.success(request, 'Your password has been reset successfully. Please sign in with your new password.')
                    return redirect('SignIn')
                else:
                    messages.error(request, 'Password and confirm password do not match.')
            else:
                messages.error(request, 'Please fill in all the fields correctly.')
        else:
            form = ResetPasswordForm(initial={'email': email})
        context = {'form': form}
        return render(request, 'reset_password.html', context)
    except ForgotPassword.DoesNotExist:
        return redirect('forgot_password')

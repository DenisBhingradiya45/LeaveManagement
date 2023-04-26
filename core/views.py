from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.urls import reverse_lazy

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


def RequestLeave(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['reason']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            user = request.user
            leave = Application.objects.create(
                user=user,
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )
            return redirect('/DashBoard/')
        return render(request, 'RequestLeave.html')
    else:
        return redirect('/SignIn/')
    
def view_leaves(request):
    student = request.user.student
    leaves = Application.objects.filter(user=student)
    return render(request, '', {'leaves': leaves})

def DashBoard(request):
    # user = request.user
    # form = user.objects.all()
    # print(form,"=================")
    return render(request, 'DashBoard.html')



class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
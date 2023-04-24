from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import *
from django.http import HttpResponse
# Create your views here.

def SignUp(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/DashBoard/')
            # else:
            #     return HttpResponse({'messages':'asdffffffff'})
        else:
            form = CustomUserCreationForm()
        return render(request, 'SignUp.html', {'form': form})
    else:
        return redirect('/DashBoard/')

def SignIn(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('/DashBoard/')
        else:
            form = AuthenticationForm()
        return render(request, 'SignIn.html', {'form': form})
    else:
        return redirect('/DashBoard/')


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
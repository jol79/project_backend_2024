from django.shortcuts import render, redirect, get_list_or_404
from django.contrib import messages

from .forms import UserRegisterForm
from .decorators import unauthenticated, authenticated
from nessues_app.models import (
    Room, Task, Nessues_Group_User, Invitation)

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


@authenticated
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'nessues_app_users/register.html', {'form': form, 'title': 'register'})


@authenticated
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'User {username} successfully authenticated!')
                return redirect('home')
            messages.error(request, 'No user with provided credentials found')
        messages.error(request, 'Form is not valid')
    form = AuthenticationForm()
    return render(request, 'nessues_app_users/login.html', {'form': form, 'title': 'login'})


@unauthenticated
def logout_view(request):
    logout(request)
    messages.info(request, 'You are successfully logged out!')
    return redirect('home')


@login_required(login_url='/login')
def account_view(request):
    rooms_stats = Room.objects.filter(owner=request.user.id).count()
    groups_stats = Nessues_Group_User.objects.filter(user=request.user.id).count()
    invitations_received = Invitation.objects.filter(user=request.user.id)

    content = {
        'rooms_stats': rooms_stats,
        'groups_stats': groups_stats,
        'invitations_received': invitations_received
    }

    return render(request, 'nessues_app_users/account.html', context=content)


def error_404_view(request, exception):
    content = {}

    return render(request, 'nessues_app_users/error_404.html', context=content)
        


# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, OwnerRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def landing_page(request):
    return render(request, 'users/landing_page.html')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register_user.html', {'form': form})

def register_owner(request):
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['owner_type']
            user.save()
            login(request, user)
            return redirect('landing_page')
    else:
        form = OwnerRegistrationForm()
    return render(request, 'users/register_owner.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'customer':
                    return redirect('user_dashboard')
                elif user.role == 'restaurant_owner':
                    return redirect('restaurant_owner_dashboard')
                elif user.role == 'grocery_owner':
                    return redirect('grocery_owner_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def login_owner(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'restaurant_owner':
                    return redirect('restaurant_owner_dashboard')
                elif user.role == 'grocery_owner':
                    return redirect('grocery_owner_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_dashboard(request):
    return render(request, 'users/user_dashboard.html')

@login_required
def restaurant_owner_dashboard(request):
    return render(request, 'users/restaurant_owner_dashboard.html')

@login_required
def grocery_owner_dashboard(request):
    return render(request, 'users/grocery_owner_dashboard.html')


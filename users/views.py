# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, OwnerRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# users/views.py (update this view)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from restaurant.forms import RestaurantForm, MenuItemForm 
from restaurant.models import Restaurant
from django.contrib.auth import logout

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
    restaurant = Restaurant.objects.get(owner=request.user)
    form = RestaurantForm(instance=restaurant)

    return render(request, 'users/restaurant_owner_dashboard.html', {
        'restaurant': restaurant,
        'form': form
    })

# Handle restaurant info editing
def edit_restaurant_info(request):
    restaurant = Restaurant.objects.get(owner=request.user)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant_owner_dashboard')
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'users/restaurant_owner_dashboard.html', {'form': form})

# Handle visibility toggling
def toggle_visibility(request):
    restaurant = Restaurant.objects.get(owner=request.user)
    if request.method == 'POST':
        restaurant.is_visible = request.POST.get('is_visible') == 'on'
        restaurant.save()
    return redirect('restaurant_owner_dashboard')

@login_required
def grocery_owner_dashboard(request):
    return render(request, 'users/grocery_owner_dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('landing_page')


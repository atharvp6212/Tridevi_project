# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, OwnerRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from restaurant.forms import RestaurantForm, MenuItemForm 
from restaurant.models import Restaurant
from django.contrib.auth import logout
from grocery.models import GroceryStore
from django.contrib.auth import get_user_model
from .forms import UserProfileForm

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

@login_required
def edit_profile(request):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')  # Redirect to the user dashboard or any other page
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})

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
    # Check if 'mode' is passed via GET to determine which mode the user is in.
    mode = request.GET.get('mode', 'restaurant')  # Default to restaurant mode
    
    if mode == 'restaurant':
        # Fetch all visible restaurants
        visible_restaurants = Restaurant.objects.filter(is_visible=True)
        context = {
            'restaurants': visible_restaurants,
            'mode': 'restaurant'  # Pass the mode to template for display logic
        }
    else:
        # Fetch all visible grocery stores
        visible_grocery_stores = GroceryStore.objects.filter(is_visible=True)
        context = {
            'grocery_stores': visible_grocery_stores,
            'mode': 'grocery'  # Pass the mode to template for display logic
        }
    
    # Fetch user information to pass to the template
    User = get_user_model()
    user = request.user
    
    context.update({
        'user': user
    })
    
    return render(request, 'users/user_dashboard.html', context)


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


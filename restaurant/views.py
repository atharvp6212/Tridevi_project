# restaurant/views.py
from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required
from .models import MenuItem
from .forms import MenuItemForm

@login_required
def restaurant_dashboard(request):
    try:
        restaurant = request.user.restaurant  # Get the current owner's restaurant
    except Restaurant.DoesNotExist:
        restaurant = None

    if request.method == 'POST':
        if restaurant:
            form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        else:
            form = RestaurantForm(request.POST, request.FILES)
            form.instance.owner = request.user  # Set the owner to the current user

        if form.is_valid():
            form.save()
            return redirect('restaurant_dashboard')
    else:
        form = RestaurantForm(instance=restaurant)

    context = {
        'form': form,
        'restaurant': restaurant,
    }
    return render(request, 'restaurant/restaurant_dashboard.html', context)


def manage_menu(request):
    restaurant = request.user.restaurant  # Assuming owner is linked to the restaurant
    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            return redirect('manage_menu')
    else:
        form = MenuItemForm()

    return render(request, 'restaurant/manage_menu.html', {'menu_items': menu_items, 'form': form})

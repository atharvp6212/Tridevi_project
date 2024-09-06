# restaurant/views.py
from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required

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

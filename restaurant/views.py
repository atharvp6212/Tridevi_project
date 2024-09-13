# restaurant/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RestaurantForm
from django.contrib.auth.decorators import login_required
from .models import MenuItem, RestaurantReview, Restaurant, RestaurantOrder, OrderItem
from .forms import MenuItemForm, RestaurantReviewForm, RestaurantOrderForm, OrderItemForm
from itertools import groupby
from operator import attrgetter
from django.urls import reverse
from decimal import Decimal
from django.core.paginator import Paginator

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


def manage_menu(request, item_id=None):
    restaurant = request.user.restaurant  # Assuming owner is linked to the restaurant
    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    if item_id:
        # Editing existing item
        menu_item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)
    else:
        # Adding a new item
        menu_item = None

    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            return redirect('manage_menu')
    else:
        form = MenuItemForm(instance=menu_item)

    return render(request, 'restaurant/manage_menu.html', {'menu_items': menu_items, 'form': form, 'editing_item': menu_item})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant).order_by('category')  # Order by category

    # Group menu items by category
    grouped_menu_items = {category: list(items) for category, items in groupby(menu_items, key=attrgetter('category'))}

    context = {
        'restaurant': restaurant,
        'grouped_menu_items': grouped_menu_items,
        'reviews': RestaurantReview.objects.filter(restaurant=restaurant)
    }
    return render(request, 'restaurant/restaurant_detail.html', context)

def restaurant_reviews(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reviews = RestaurantReview.objects.filter(restaurant=restaurant)
    if request.method == 'POST':
        form = RestaurantReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user  # Assign the logged-in user
            review.restaurant = restaurant  # Link review to the restaurant
            review.save()
            return redirect('restaurant_reviews', restaurant_id=restaurant.id)  # Refresh the page after submission
    else:
        form = RestaurantReviewForm()

    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'form': form  # Include the form in the context
    }
    return render(request, 'restaurant/restaurant_reviews.html', context)

def restaurant_search(request):
    query = request.GET.get('q')
    if query:
        results = Restaurant.objects.filter(name__icontains=query)  # Searches by name
    else:
        results = Restaurant.objects.all()

    return render(request, 'restaurant/restaurant_search_results.html', {'results': results})

def place_restaurant_order(request, restaurant_id):
    if request.method == 'POST':
        order_items = request.session.get('order_items', [])
        total_price = Decimal(request.session.get('total_price', 0))

        for key, value in request.POST.items():
            if key.startswith('item_'):
                item_id = key.split('_')[1]
                quantity = int(value)
                if quantity > 0:
                    item = get_object_or_404(MenuItem, id=item_id)
                    price = item.price * quantity
                    total_price += price
                    
                    # Check if item is already in the order_items
                    existing_item = next((item for item in order_items if item['id'] == item.id), None)
                    if existing_item:
                        existing_item['quantity'] += quantity
                        existing_item['price'] = str(item.price * existing_item['quantity'])  # Update total price for the item
                    else:
                        order_items.append({
                            'id': item.id,
                            'name': item.name,
                            'quantity': quantity,
                            'price': str(price)  # Convert price to string
                        })

        # Store updated order details in session
        request.session['order_items'] = order_items
        request.session['total_price'] = str(total_price)  # Convert total price to string
        request.session['restaurant_id'] = restaurant_id
        
        return redirect('confirm_order')  # Redirect to confirmation view

def confirm_order(request):
    order_items = request.session.get('order_items', [])
    total_price = Decimal(request.session.get('total_price', 0))
    restaurant_id = request.session.get('restaurant_id')
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            # Create the order if confirmed
            order = RestaurantOrder.objects.create(customer=request.user, restaurant=restaurant, total_price=total_price)
            
            for item in order_items:
                menu_item = get_object_or_404(MenuItem, id=item['id'])
                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=item['quantity'], price=item['price'])

            # Clear the session data
            del request.session['order_items']
            del request.session['total_price']
            del request.session['restaurant_id']
            
            return redirect('restaurant_detail', restaurant_id=restaurant.id)

        elif 'update' in request.POST:
            # Update quantities based on user input
            for item in order_items:
                quantity = int(request.POST.get(f'quantity_{item["id"]}', 0))
                item['quantity'] = quantity
                item['price'] = str(Decimal(item['price']) / item['quantity'] * quantity)  # Update price based on new quantity

            # Recalculate total price
            total_price = sum(Decimal(item['price']) for item in order_items)
            request.session['total_price'] = str(total_price)  # Update total price in session

    return render(request, 'restaurant/order_confirmation.html', {
        'order_items': order_items,
        'total_price': total_price,
        'restaurant': restaurant
    })
    
def remove_item(request, item_id):
    order_items = request.session.get('order_items', [])
    order_items = [item for item in order_items if item['id'] != item_id]  # Remove the item
    request.session['order_items'] = order_items  # Update session
    return redirect('confirm_order')  # Redirect to confirmation page

    
def manage_restaurant_orders(request):
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    
    pending_orders = RestaurantOrder.objects.filter(restaurant=restaurant, status='Pending')
    completed_orders = RestaurantOrder.objects.filter(restaurant=restaurant, status='Completed').order_by('-order_date')

    # Prepare a list of (order, items) tuples for pending orders
    pending_order_items = [(order, OrderItem.objects.filter(order=order)) for order in pending_orders]

    # Pagination for completed orders
    paginator = Paginator(completed_orders, 5)  # Show 5 completed orders per page
    page_number = request.GET.get('page')  # Get the page number from the URL
    completed_orders_page = paginator.get_page(page_number)  # Get the orders for the current page

    # Prepare a list of (order, items) tuples for completed orders on the current page
    completed_order_items = [(order, OrderItem.objects.filter(order=order)) for order in completed_orders_page]

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        
        if order_id and action in ['accept', 'reject']:
            order = get_object_or_404(RestaurantOrder, id=order_id, restaurant=restaurant)
            if action == 'accept':
                order.status = 'Completed'
                order.save()  # Save the order status change
            elif action == 'reject':
                order.delete()  # Delete the order
            
            return redirect('manage_restaurant_orders')  # Redirect to refresh the page
    
    context = {
        'pending_orders': pending_order_items,
        'completed_orders': completed_order_items,
        'completed_orders_page': completed_orders_page,
    }
    return render(request, 'restaurant/manage_restaurant_orders.html', context)
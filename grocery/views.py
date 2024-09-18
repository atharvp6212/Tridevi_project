# grocery/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GroceryStore
from .forms import GroceryStoreForm
from .models import Product, GroceryReview
from .forms import ProductForm, GroceryReviewForm,GroceryOrderForm, GroceryOrderItemForm
from .models import GroceryStore,GroceryOrder, GroceryOrderItem
from .forms import GroceryOrderForm, GroceryOrderItemForm
from django.core.paginator import Paginator

@login_required
def grocery_owner_dashboard(request):
    # Attempt to get the grocery store associated with the logged-in user
    try:
        grocery_store = GroceryStore.objects.get(owner=request.user)
    except GroceryStore.DoesNotExist:
        # Redirect to a page where they can create a grocery store or show an error message
        return redirect('create_grocery_store')  # Adjust this to your actual URL name for creating a grocery store

    form = GroceryStoreForm(instance=grocery_store)

    return render(request, 'users/grocery_owner_dashboard.html', {
        'grocery_store': grocery_store,
        'form': form
    })
    
@login_required
def create_grocery_store(request):
    if request.method == 'POST':
        form = GroceryStoreForm(request.POST)
        if form.is_valid():
            grocery_store = form.save(commit=False)
            grocery_store.owner = request.user  # Set the owner of the grocery store
            grocery_store.save()
            return redirect('grocery_owner_dashboard')  # Redirect after creation
    else:
        form = GroceryStoreForm()

    return render(request, 'users/create_grocery_store.html', {'form': form})


# Handle grocery info editing
def edit_grocery_info(request):
    grocery_store = GroceryStore.objects.get(owner=request.user)
    if request.method == 'POST':
        form = GroceryStoreForm(request.POST, request.FILES, instance=grocery_store)
        if form.is_valid():
            form.save()
            return redirect('grocery_owner_dashboard')
    else:
        form = GroceryStoreForm(instance=grocery_store)
    return render(request, 'users/grocery_owner_dashboard.html', {'form': form})

# Handle visibility toggling
def toggle_grocery_visibility(request):
    grocery_store = GroceryStore.objects.get(owner=request.user)
    if request.method == 'POST':
        grocery_store.is_visible = request.POST.get('is_visible') == 'on'
        grocery_store.save()
    return redirect('grocery_owner_dashboard')

@login_required
def manage_product_list(request):
    try:
        grocery_store = request.user.grocerystore  # Correct attribute access
    except GroceryStore.DoesNotExist:
        return redirect('grocery_owner_dashboard')  # Handle case where user has no store

    products = Product.objects.filter(grocery_store=grocery_store)

    # Check if we are editing a product
    product_id = request.GET.get('edit')
    if product_id:
        product = get_object_or_404(Product, id=product_id, grocery_store=grocery_store)
        form = ProductForm(instance=product)
    else:
        product = None
        form = ProductForm()

    if request.method == 'POST':
        if product:
            form = ProductForm(request.POST, instance=product)  # Update existing product
        else:
            form = ProductForm(request.POST)  # Add a new product

        if form.is_valid():
            product = form.save(commit=False)
            product.grocery_store = grocery_store
            product.save()
            return redirect('manage_product_list')

    return render(request, 'grocery/manage_product_list.html', {
        'products': products,
        'form': form,
        'editing_product': product,
    })


def grocery_detail(request, grocery_id):
    grocery_store = get_object_or_404(GroceryStore, id=grocery_id)
    products = Product.objects.filter(grocery_store=grocery_store, stock__gt=25)  # Fetch store's products
    context = {
        'grocery_store': grocery_store,
        'products': products,
        'reviews': GroceryReview.objects.filter(grocery_store=grocery_store),
    }
    return render(request, 'grocery/grocery_detail.html', context)

def grocery_reviews(request, grocery_id):
    grocery_store = get_object_or_404(GroceryStore, id=grocery_id)
    reviews = GroceryReview.objects.filter(grocery_store=grocery_store)
    if request.method == 'POST':
        form = GroceryReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user  # Assign the logged-in user
            review.grocery_store = grocery_store  # Link review to the grocery store
            review.save()
            return redirect('grocery_reviews', grocery_id=grocery_store.id)  # Refresh the page after submission
    else:
        form = GroceryReviewForm()

    context = {
        'grocery_store': grocery_store,
        'reviews': reviews,
        'form': form  # Include the form in the context
    }
    return render(request, 'grocery/grocery_reviews.html', context)

def grocery_search(request):
    query = request.GET.get('q')
    if query:
        results = GroceryStore.objects.filter(name__icontains=query)  # Searches by name
    else:
        results = GroceryStore.objects.all()

    return render(request, 'grocery/grocery_search_results.html', {'results': results})


def place_grocery_order(request, grocery_id):
    if request.method == 'POST':
        grocery_store = get_object_or_404(GroceryStore, id=grocery_id)
        order = GroceryOrder.objects.create(customer=request.user, store=grocery_store)

        total_price = 0
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                quantity = int(value)

                product = get_object_or_404(Product, id=product_id)
                price = product.price * quantity
                total_price += price
                GroceryOrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

        order.total_price = total_price
        order.save()

        return redirect('order_confirmation', order_id=order.id)
    
    return redirect('grocery_detail', grocery_id=grocery_id)
    

def review_order(request, grocery_id):
    if request.method == 'POST':
        grocery_store = get_object_or_404(GroceryStore, id=grocery_id)
        order_items = []

        total_price = 0
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                quantity = int(value)

                product = get_object_or_404(Product, id=product_id)
                price = product.price * quantity
                total_price += price
                order_items.append((product, quantity, price))

        context = {
            'grocery_store': grocery_store,
            'order_items': order_items,
            'total_price': total_price,
        }
        return render(request, 'grocery/review_order.html', context)

    return redirect('grocery_detail', grocery_id=grocery_id)

def order_confirmation(request, order_id):
    order = get_object_or_404(GroceryOrder, id=order_id)
    order_items = GroceryOrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'grocery/order_confirmation.html', context)

def remove_from_cart(request, product_id):
    order_id = request.session.get('order_id')
    if order_id:
        order = get_object_or_404(GroceryOrder, id=order_id)
        order_item = get_object_or_404(GroceryOrderItem, order=order, product_id=product_id)
        order_item.delete()
        return redirect('review_order', grocery_id=order.store.id)
    
    return redirect('grocery_detail', grocery_id=order.store.id)

    
def manage_grocery_orders(request):
    store = get_object_or_404(GroceryStore, owner=request.user)
    
    pending_orders = GroceryOrder.objects.filter(store=store, status='Pending')
    completed_orders = GroceryOrder.objects.filter(store=store, status='Completed').order_by('-order_date')

    # Prepare a list of (order, items) tuples for pending orders
    pending_order_items = [(order, GroceryOrderItem.objects.filter(order=order)) for order in pending_orders]

    # Pagination for completed orders
    paginator = Paginator(GroceryOrder.objects.filter(store=store, status='Completed'), 5)  # 5 orders per page
    page_number = request.GET.get('page')
    completed_orders_page = paginator.get_page(page_number)

    # Prepare a list of (order, items) tuples for completed orders on the current page
    completed_order_items = [(order, GroceryOrderItem.objects.filter(order=order)) for order in completed_orders_page]

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        
        if order_id and action in ['accept', 'reject']:
            order = get_object_or_404(GroceryOrder, id=order_id, store=store)
            if action == 'accept':
                order.status = 'Completed'
                order.save()  # Save the order status change
            elif action == 'reject':
                GroceryOrderItem.objects.filter(order=order).delete()  # Delete related order items
                order.delete()  # Now delete the order
            
            return redirect('manage_grocery_orders')  # Redirect to refresh the page
    
    context = {
        'pending_orders': pending_order_items,
        'completed_orders': completed_order_items,
        'completed_orders_page': completed_orders_page,
    }
    return render(request, 'grocery/manage_grocery_orders.html', context)
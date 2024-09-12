# grocery/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GroceryStore
from .forms import GroceryStoreForm
from .models import Product, GroceryReview
from .forms import ProductForm, GroceryReviewForm,GroceryOrderForm, GroceryOrderItemForm
from .models import GroceryStore,GroceryOrder, GroceryOrderItem
from .forms import GroceryOrderForm, GroceryOrderItemForm

@login_required
def grocery_owner_dashboard(request):
    grocery_store = GroceryStore.objects.get(owner=request.user)
    form = GroceryStoreForm(instance=grocery_store)

    return render(request, 'users/grocery_owner_dashboard.html', {
        'grocery_store': grocery_store,
        'form': form
    })

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
                
                if quantity > 0:  # Only process items with a quantity greater than 0
                    product = get_object_or_404(Product, id=product_id)
                    price = product.price * quantity
                    total_price += price
                    GroceryOrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
        
        order.total_price = total_price
        order.save()
        
        return redirect('grocery_detail', grocery_id=grocery_store.id)



    
def manage_grocery_orders(request):
    store = get_object_or_404(GroceryStore, owner=request.user)
    
    pending_orders = GroceryOrder.objects.filter(store=store, status='Pending')
    completed_orders = GroceryOrder.objects.filter(store=store, status='Completed')

    # Prepare a list of (order, items) tuples
    pending_order_items = [(order, GroceryOrderItem.objects.filter(order=order)) for order in pending_orders]
    completed_order_items = [(order, GroceryOrderItem.objects.filter(order=order)) for order in completed_orders]

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        
        if order_id and action in ['accept', 'reject']:
            order = get_object_or_404(GroceryOrder, id=order_id, store=store)
            if action == 'accept':
                order.status = 'Completed'
            elif action == 'reject':
                order.delete()
            
            order.save()
            return redirect('manage_grocery_orders')
    
    context = {
        'pending_orders': pending_order_items,
        'completed_orders': completed_order_items,
    }
    return render(request, 'grocery/manage_grocery_orders.html', context)
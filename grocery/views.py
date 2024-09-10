# grocery/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GroceryStore
from .forms import GroceryStoreForm
from .models import Product
from .forms import ProductForm

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

def manage_product_list(request):
    try:
        grocery_store = request.user.grocerystore  # Correct attribute access
    except GroceryStore.DoesNotExist:
        return redirect('grocery_owner_dashboard')  # Handle case where user has no store

    products = Product.objects.filter(grocery_store=grocery_store)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.grocery_store = grocery_store
            product.save()
            return redirect('manage_product_list')
    else:
        form = ProductForm()

    return render(request, 'grocery/manage_product_list.html', {'products': products, 'form': form})

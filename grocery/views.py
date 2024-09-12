# grocery/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GroceryStore
from .forms import GroceryStoreForm
from .models import Product, GroceryReview
from .forms import ProductForm, GroceryReviewForm

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

def grocery_detail(request, grocery_id):
    grocery_store = get_object_or_404(GroceryStore, id=grocery_id)
    products = Product.objects.filter(grocery_store=grocery_store)  # Fetch store's products
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

# grocery/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GroceryStore
from .forms import GroceryStoreForm

@login_required
def grocery_owner_dashboard(request):
    try:
        grocery_store = GroceryStore.objects.get(owner=request.user)
    except GroceryStore.DoesNotExist:
        grocery_store = None

    if request.method == 'POST':
        form = GroceryStoreForm(request.POST, request.FILES, instance=grocery_store)
        if form.is_valid():
            grocery_store = form.save(commit=False)
            grocery_store.owner = request.user
            grocery_store.save()
            return redirect('grocery_owner_dashboard')
    else:
        form = GroceryStoreForm(instance=grocery_store)

    return render(request, 'users/grocery_owner_dashboard.html', {'form': form, 'grocery_store': grocery_store})

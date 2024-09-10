# grocery/forms.py
from django import forms
from .models import GroceryStore
from .models import Product

class GroceryStoreForm(forms.ModelForm):
    class Meta:
        model = GroceryStore
        fields = ['name', 'phone', 'address', 'logo']
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']

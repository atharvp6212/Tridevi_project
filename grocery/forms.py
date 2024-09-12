# grocery/forms.py
from django import forms
from .models import GroceryStore
from .models import Product,GroceryReview, GroceryStore, GroceryOrder, GroceryOrderItem

class GroceryStoreForm(forms.ModelForm):
    class Meta:
        model = GroceryStore
        fields = ['name', 'phone', 'address', 'logo','offers_gold']
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
        
class GroceryReviewForm(forms.ModelForm):
    class Meta:
        model = GroceryReview
        fields = ['review_text', 'rating']


class GroceryOrderForm(forms.ModelForm):
    class Meta:
        model = GroceryOrder
        fields = ['store']  # You can customize as needed

class GroceryOrderItemForm(forms.ModelForm):
    class Meta:
        model = GroceryOrderItem
        fields = ['product', 'quantity']
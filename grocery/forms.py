# grocery/forms.py
from django import forms
from .models import GroceryStore
from .models import Product,GroceryReview, GroceryStore

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

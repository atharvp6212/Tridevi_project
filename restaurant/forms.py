# restaurant/forms.py
from django import forms
from .models import MenuItem,RestaurantReview, Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'phone', 'address', 'veg', 'non_veg', 'logo','offers_gold']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'is_veg']
        
class RestaurantReviewForm(forms.ModelForm):
    class Meta:
        model = RestaurantReview
        fields = ['review_text', 'rating']
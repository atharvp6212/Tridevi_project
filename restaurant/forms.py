# restaurant/forms.py
from django import forms
from .models import MenuItem,RestaurantReview, Restaurant, RestaurantOrder, OrderItem

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'phone', 'address', 'veg', 'non_veg', 'logo','offers_gold']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'is_veg', 'category']
        
class RestaurantReviewForm(forms.ModelForm):
    class Meta:
        model = RestaurantReview
        fields = ['review_text', 'rating']
        
class RestaurantOrderForm(forms.ModelForm):
    class Meta:
        model = RestaurantOrder
        fields = ['customer', 'restaurant', 'total_price']  # You can customize as needed

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']
# restaurant/forms.py
from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'phone', 'address', 'veg', 'non_veg', 'logo']

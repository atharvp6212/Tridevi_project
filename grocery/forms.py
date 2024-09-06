# grocery/forms.py
from django import forms
from .models import GroceryStore

class GroceryStoreForm(forms.ModelForm):
    class Meta:
        model = GroceryStore
        fields = ['name', 'phone', 'address', 'logo']

# grocery/models.py
from django.db import models
from django.contrib.auth import get_user_model

class GroceryStore(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    store_type = models.CharField(max_length=10, choices=[('veg', 'Veg'), ('non_veg', 'Non-Veg'), ('both', 'Both')])
    logo = models.ImageField(upload_to='grocery_logos/', blank=True, null=True)
    offers_gold = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    grocery_store = models.ForeignKey('GroceryStore', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

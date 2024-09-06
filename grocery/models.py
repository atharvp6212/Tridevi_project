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

    def __str__(self):
        return self.name

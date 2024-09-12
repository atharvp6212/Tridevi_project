# grocery/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User

class GroceryStore(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    store_type = models.CharField(max_length=10, choices=[('veg', 'Veg'), ('non_veg', 'Non-Veg'), ('both', 'Both')])
    logo = models.ImageField(upload_to='grocery_logos/', blank=True, null=True)
    offers_gold = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    working_hours = models.CharField(max_length=100, default="9 AM - 9 PM")

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

class GroceryReview(models.Model):
    grocery_store = models.ForeignKey(GroceryStore, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL
    review_text = models.TextField()
    rating = models.IntegerField()  # Rating out of 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username}'s review for {self.grocery_store.name}"

class GroceryOrder(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(GroceryStore, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='GroceryOrderItem')  # Updated to use Product
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, Completed

class GroceryOrderItem(models.Model):
    order = models.ForeignKey(GroceryOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Updated to use Product
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

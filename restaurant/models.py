# restaurant/models.py
from django.db import models
from users.models import CustomUser
from django.conf import settings
from django.contrib.auth.models import User

class Restaurant(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    veg = models.BooleanField(default=False)
    non_veg = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)
    offers_gold = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    working_hours = models.CharField(max_length=100,  default="9 AM - 9 PM")

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_veg = models.BooleanField(default=True)
    category = models.CharField(max_length=100, default='general')

    def __str__(self):
        return self.name

class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL
    review_text = models.TextField()
    rating = models.IntegerField()  # Rating out of 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username}'s review for {self.restaurant.name}"
    

class RestaurantOrder(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, Completed

class OrderItem(models.Model):
    order = models.ForeignKey(RestaurantOrder, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Coupon(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='coupons')
    name = models.CharField(max_length=100, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 10.00 for 10%

    def __str__(self):
        return self.name
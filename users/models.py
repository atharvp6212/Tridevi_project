# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('restaurant_owner', 'Restaurant Owner'),
        ('grocery_owner', 'Grocery Store Owner'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    gold_member = models.BooleanField(default=False)

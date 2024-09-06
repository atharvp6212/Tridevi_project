# restaurant/models.py
from django.db import models
from users.models import CustomUser

class Restaurant(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    veg = models.BooleanField(default=False)
    non_veg = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

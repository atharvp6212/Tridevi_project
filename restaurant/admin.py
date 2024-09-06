from django.contrib import admin
from .models import Restaurant

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'veg', 'non_veg', 'logo')
    search_fields = ('name', 'address')
    list_filter = ('veg', 'non_veg')

admin.site.register(Restaurant, RestaurantAdmin)

from django.contrib import admin
from .models import GroceryStore

class GroceryStoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'store_type', 'logo')
    search_fields = ('name', 'address')
    list_filter = ('store_type',)

admin.site.register(GroceryStore, GroceryStoreAdmin)

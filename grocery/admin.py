from django.contrib import admin
from .models import GroceryStore, Product

# Define an inline admin descriptor for Product model
# which acts a bit like a reverse ForeignKey to GroceryStore.
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1  # Number of extra empty fields to display for new products

# Define the admin class for GroceryStore
class GroceryStoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'store_type', 'logo', 'offers_gold')
    search_fields = ('name', 'address')
    list_filter = ('store_type',)
    inlines = [ProductInline]  # This will display the products inline

# Register the models in admin interface
admin.site.register(GroceryStore, GroceryStoreAdmin)

# Keep the Product admin for separate management of Products
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'grocery_store', 'price', 'stock']
    search_fields = ['name', 'grocery_store__name']

admin.site.register(Product, ProductAdmin)

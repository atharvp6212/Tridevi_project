from django.contrib import admin
from .models import Restaurant, MenuItem, RestaurantReview

# Define an inline admin descriptor for MenuItem model
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1  # This allows one extra blank item for adding new menu items

# Define the admin class for Restaurant
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'veg', 'non_veg', 'logo', 'offers_gold')
    search_fields = ('name', 'address')
    list_filter = ('veg', 'non_veg')
    inlines = [MenuItemInline]  # This will display the menu items inline

# Register the models in the admin interface
admin.site.register(Restaurant, RestaurantAdmin)

# Keep the MenuItem admin for separate management of Menu Items
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'price', 'is_veg']
    search_fields = ['name', 'restaurant__name']

admin.site.register(MenuItem, MenuItemAdmin)

class RestaurantReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'customer', 'rating', 'review_text', 'created_at')
    search_fields = ('restaurant__name', 'customer__username', 'review_text')
    list_filter = ('rating', 'created_at')

admin.site.register(RestaurantReview, RestaurantReviewAdmin)

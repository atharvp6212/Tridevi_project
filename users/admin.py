from django.contrib import admin
from django.contrib.auth import get_user_model
from grocery.models import GroceryStore
from restaurant.models import Restaurant
from django.utils.html import format_html

User = get_user_model()

class RestaurantOwnerInline(admin.TabularInline):
    model = Restaurant
    fields = ('name', 'phone', 'address', 'store_type', 'logo', 'offers_gold', 'is_visible')
    extra = 0
    can_delete = False
    verbose_name = 'Restaurant Owner Details'
    verbose_name_plural = 'Restaurant Owner Details'

# Inline admin for Grocery Store Owner
class GroceryStoreOwnerInline(admin.TabularInline):
    model = GroceryStore
    fields = ('name', 'phone', 'address', 'store_type', 'logo', 'offers_gold', 'is_visible')
    extra = 0
    can_delete = False
    verbose_name = 'Grocery Store Owner Details'
    verbose_name_plural = 'Grocery Store Owner Details'

# Custom admin for User
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 
        'first_name', 
        'last_name', 
        'email', 
        'phone', 
        'profile_picture_display',
        'user_type'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    def get_inlines(self, request, obj=None):
        """
        Return different inlines based on the user type.
        """
        inlines = []
        if request.user.is_superuser:
            if hasattr(obj, 'restaurant'):
                inlines = [RestaurantOwnerInline]
            elif hasattr(obj, 'grocery_store'):
                inlines = [GroceryStoreOwnerInline]
        return inlines

    def profile_picture_display(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;">', obj.profile_picture.url)
        return "No image"
    
    profile_picture_display.short_description = 'Profile Picture'

    def user_type(self, obj):
        if hasattr(obj, 'restaurant'):
            return 'Restaurant Owner'
        elif hasattr(obj, 'grocery_store'):
            return 'Grocery Store Owner'
        else:
            return 'Customer'
    
    user_type.short_description = 'User Type'

admin.site.register(User, CustomUserAdmin)
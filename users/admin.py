# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    # Adding only the custom field ('role') to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Only add 'role', since the rest are already in UserAdmin
    )

    # Defining fields when creating a new user in the admin panel
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register the CustomUser model in the admin panel
admin.site.register(CustomUser, CustomUserAdmin)

# grocery/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import manage_product_list

urlpatterns = [
    path('grocery_owner_dashboard/', views.grocery_owner_dashboard, name='grocery_owner_dashboard'),
    path('manage-product-list/', views.manage_product_list, name='manage_product_list'),
    path('edit-info/', views.edit_grocery_info, name='edit_grocery_info'),
    path('toggle-visibility/', views.toggle_grocery_visibility, name='toggle_grocery_visibility'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('grocery/<int:grocery_id>/', views.grocery_detail, name='grocery_detail'),
]

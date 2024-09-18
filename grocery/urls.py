# grocery/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import manage_product_list
from users.views import create_grocery_store

urlpatterns = [
    path('grocery_owner_dashboard/', views.grocery_owner_dashboard, name='grocery_owner_dashboard'),
    path('manage-product-list/', views.manage_product_list, name='manage_product_list'),
    path('edit-info/', views.edit_grocery_info, name='edit_grocery_info'),
    path('toggle-visibility/', views.toggle_grocery_visibility, name='toggle_grocery_visibility'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('grocery/<int:grocery_id>/', views.grocery_detail, name='grocery_detail'),
    path('grocery/<int:grocery_id>/reviews/', views.grocery_reviews, name='grocery_reviews'),
    path('search/', views.grocery_search, name='grocery_search'),
    path('grocery/orders/', views.manage_grocery_orders, name='manage_grocery_orders'),
    path('grocery/<int:grocery_id>/order/', views.place_grocery_order, name='place_grocery_order'),
    path('grocery/<int:grocery_id>/review/', views.review_order, name='review_order'),
    path('order/<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('create-grocery-store/', create_grocery_store, name='create_grocery_store'),
]

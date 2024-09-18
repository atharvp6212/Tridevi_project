# users/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import create_restaurant, create_grocery_store


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register_user/', views.register_user, name='register_user'),
    path('register_owner/', views.register_owner, name='register_owner'),
    path('login_user/', views.login_user, name='login_user'),
    path('login_owner/', views.login_owner, name='login_owner'),
    path('login/', views.login_user, name='login'),  # Add this for /users/login/
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('restaurant_owner_dashboard/', views.restaurant_owner_dashboard, name='restaurant_owner_dashboard'),
    path('grocery_owner_dashboard/', views.grocery_owner_dashboard, name='grocery_owner_dashboard'),
    path('edit-info/', views.edit_restaurant_info, name='edit_restaurant_info'),
    path('toggle-visibility/', views.toggle_visibility, name='toggle_visibility'), 
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create-restaurant/', create_restaurant, name='create_restaurant'),
    path('create-grocery-store/', create_grocery_store, name='create_grocery_store'),
]

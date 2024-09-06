# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register_user/', views.register_user, name='register_user'),
    path('register_owner/', views.register_owner, name='register_owner'),
    path('login_user/', views.login_user, name='login_user'),
    path('login_owner/', views.login_owner, name='login_owner'),  
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('restaurant_owner_dashboard/', views.restaurant_owner_dashboard, name='restaurant_owner_dashboard'),
    path('grocery_owner_dashboard/', views.grocery_owner_dashboard, name='grocery_owner_dashboard'),  
]

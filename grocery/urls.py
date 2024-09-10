# grocery/urls.py
from django.urls import path
from . import views
from .views import manage_product_list

urlpatterns = [
    path('grocery_owner_dashboard/', views.grocery_owner_dashboard, name='grocery_owner_dashboard'),
    path('manage-product-list/', views.manage_product_list, name='manage_product_list'),
]

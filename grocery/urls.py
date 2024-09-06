# grocery/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('grocery_owner_dashboard/', views.grocery_owner_dashboard, name='grocery_owner_dashboard'),
]

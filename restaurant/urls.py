# urls.py in restaurant app
from django.urls import path
from .views import manage_menu
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('manage-menu/', views.manage_menu, name='manage_menu'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
]
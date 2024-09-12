# urls.py in restaurant app
from django.urls import path
from .views import manage_menu
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('manage-menu/', views.manage_menu, name='manage_menu'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:restaurant_id>/reviews/', views.restaurant_reviews, name='restaurant_reviews'),
    path('search/', views.restaurant_search, name='restaurant_search'),
    path('manage-menu/<int:item_id>/', views.manage_menu, name='manage_menu_edit'),
    path('restaurant/<int:restaurant_id>/order/', views.place_restaurant_order, name='place_restaurant_order'),
    path('restaurant/orders/', views.manage_restaurant_orders, name='manage_restaurant_orders'),
]
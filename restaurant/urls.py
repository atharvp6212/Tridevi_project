# urls.py in restaurant app
from django.urls import path
from .views import manage_menu
from . import views

urlpatterns = [
    path('manage-menu/', views.manage_menu, name='manage_menu'),
]
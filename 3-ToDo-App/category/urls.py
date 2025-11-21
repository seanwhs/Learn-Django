# category app urls.py
from django.urls import path
from .views import create_category, update_category, delete_category

urlpatterns = [
    path('create/', create_category, name='create_category'),
    path('update/<int:id>/', update_category, name='update_category'),
    path('delete/<int:id>/', delete_category, name='delete_category'),
]

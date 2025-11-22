# todo app urls.py
from django.urls import path
from .views import list_tasks, create_task, update_task, delete_task

urlpatterns = [
    path('', list_tasks, name='list'),
    path('create/', create_task, name='create'),
    path('update/<int:id>/', update_task, name='update'),
    path('delete/<int:id>/', delete_task, name='delete'),
]

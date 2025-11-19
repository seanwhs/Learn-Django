# main urls.py
from blinker import Namespace
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls', namespace = 'todos'))
]

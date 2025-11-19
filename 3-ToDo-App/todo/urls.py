# todo.urls.py
from django.urls import URLPattern, path
from .views import todo_list, todo_detail, todo_create, todo_update, todo_delete

app_name = 'todos'
urlpatterns = [
    path('', todo_list, name='todo_list'),
    path('<int:todo_id>/', todo_detail, name='todo_detail'),
    path('create/', todo_create, name='create'),
    path('<int:todo_id>/update/', todo_update, name='update'),
    path('<int:todo_id>/delete/', todo_delete, name='delete'),
]
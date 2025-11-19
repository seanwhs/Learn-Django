# todo.views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Todo
from .forms import TodoForm

def todo_list(request):
    todos = Todo.objects.all()
    print(todos)
    context = {
        'todo_list': todos
    }
    return render(request, 'todo_list.html', context)

def todo_detail(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    context = {'todo': todo }
    return render (request, 'todo_detail.html', context)

def todo_create(request):
    form = TodoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/')  # redirect after saving

    context = {'form': form}
    return render(request, 'todo_create.html', context)

def todo_update(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    form = TodoForm(request.POST or None, instance=todo)
    if form.is_valid():
        form.save()
        return redirect('/')  # redirect after saving
    context = {'form': form}
    return render(request, 'todo_create.html', context)

def todo_delete(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return redirect('todos:todo_list')  # redirect after saving

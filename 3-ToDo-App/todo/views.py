# todo app views.py
from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from .forms import TaskForm
from category.models import Category

def list_tasks(request):
    tasks = Task.objects.all()
    categories = Category.objects.all()
    return render(request, 'task/task_list.html', {'tasks': tasks, 'categories': categories})

def create_task(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.full_clean()
        task.save()
        return redirect('list')
    return render(request, 'task/task_form.html', {'form': form, 'action': 'Create'})

def update_task(request, id):
    task = get_object_or_404(Task, id=id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        task = form.save(commit=False)
        task.full_clean()
        task.save()
        return redirect('list')
    return render(request, 'task/task_form.html', {'form': form, 'action': 'Update'})

def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.delete()
        return redirect('list')
    return render(request, 'task/task_delete.html', {'task': task, 'action': 'Delete'})

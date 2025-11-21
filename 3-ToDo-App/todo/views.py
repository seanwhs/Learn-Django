from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from category.models import Category
from .forms import TaskForm


def list_tasks(request):
    tasks = Task.objects.all()
    categories = Category.objects.all()
    return render(request, 'task/task_list.html', {
        'tasks': tasks,
        'categories': categories
    })


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = TaskForm()

    return render(request, 'task/task_form.html', {
        'form': form,
        'action': 'Create'
    })


def update_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task/task_form.html', {
        'form': form,
        'action': 'Update'
    })


def delete_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        task.delete()
        return redirect('list')

    return render(request, 'task/task_delete.html', {
        'task': task, 'action': 'Delete'
    })

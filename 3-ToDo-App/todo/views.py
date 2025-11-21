# todo app views.py
from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from category.models import Category
from .forms import TaskForm
from datetime import date, timedelta
import calendar

# -------------------------
# Helper function for recurring tasks
# -------------------------
def get_next_due(task):
    """
    Returns the next due date for a recurring task.
    If non-recurring, returns the current due_date.
    """
    if not task.due_date:
        return None  # No due date for non-recurring tasks

    if task.recurrence == 'daily':
        return task.due_date + timedelta(days=1)
    elif task.recurrence == 'weekly':
        return task.due_date + timedelta(weeks=1)
    elif task.recurrence == 'monthly':
        month = task.due_date.month + 1
        year = task.due_date.year
        day = task.due_date.day

        # handle year overflow
        if month > 12:
            month = 1
            year += 1

        # handle day overflow for months with fewer days
        last_day_of_month = calendar.monthrange(year, month)[1]
        day = min(day, last_day_of_month)

        return task.due_date.replace(year=year, month=month, day=day)
    else:
        return task.due_date

# -------------------------
# Task Views
# -------------------------
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
            task = form.save(commit=False)
            task.full_clean()  # runs model.clean()
            task.save()
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
            task = form.save(commit=False)
            task.full_clean()
            task.save()

            # Create next occurrence if recurring and task is marked done
            if task.recurrence and task.is_done:
                next_due = get_next_due(task)
                if next_due:
                    Task.objects.create(
                        category=task.category,
                        title=task.title,
                        description=task.description,
                        priority=task.priority,
                        due_date=next_due,
                        recurrence=task.recurrence,
                    )

            return redirect('list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task/task_form.html', {'form': form, 'action': 'Update'})

def delete_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        task.delete()
        return redirect('list')

    return render(request, 'task/task_delete.html', {
        'task': task, 'action': 'Delete'
    })

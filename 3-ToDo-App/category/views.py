# category app views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm

def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list')
    return render(request, 'category/category_form.html', {'form': form, 'action': 'Create'})

def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('list')
    return render(request, 'category/category_form.html', {'form': form, 'action': 'Update'})

def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('list')
    return render(request, 'category/category_delete.html', {'category': category, 'action': 'Delete'})

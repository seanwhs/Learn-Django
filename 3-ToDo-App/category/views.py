# category app views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from django import forms

# Category form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

    def clean_title(self):
        title = self.cleaned_data['title'].strip().capitalize()
        if Category.objects.filter(title__iexact=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This category already exists.")
        return title


# Create category
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')  # Redirect to task list
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form, 'action': 'Create'})


# Update category
def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form, 'action': 'Update'})


# Delete category
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('list')
    return render(request, 'category/category_delete.html', {'category': category, 'action': 'Delete'})

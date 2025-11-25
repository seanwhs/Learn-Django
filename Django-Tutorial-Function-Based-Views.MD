<!-- Django-Tutorial-Function-Based-Views.MD -->
# Django CRUDL Tutorial

This tutorial demonstrates how to create a Django CRUDL (Create, Read, Update, Delete, List) application using **Function-Based Views (FBVs)**, Django Models, and Django Forms.

## Prerequisites

- Python 3.8+
- Django 4.x+
- Basic understanding of Python and HTML

---

## Step 1: Create a Django Project

```bash
# Install Django
pip install django

# Create a new Django project
django-admin startproject myproject

# Navigate into the project
cd myproject

# Start a new app
python manage.py startapp myapp
````

---

## Step 2: Configure the Project

Add your app to `INSTALLED_APPS` in `myproject/settings.py`:

```python
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your app
    'myapp',
]
```

---

## Step 3: Create a Model

In `myapp/models.py`, define a model. We'll use a **Book** model as an example:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title
```

Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 4: Create a Django Form

In `myapp/forms.py`, create a form for the `Book` model:

```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn']
```

---

## Step 5: Create Views for CRUDL

In `myapp/views.py`, add the following views:

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm

# List all books
def book_list(request):
    books = Book.objects.all()
    return render(request, 'myapp/book_list.html', {'books': books})

# Create a new book
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'myapp/book_form.html', {'form': form})

# Update a book
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'myapp/book_form.html', {'form': form})

# Delete a book
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'myapp/book_confirm_delete.html', {'book': book})

# View book details
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'myapp/book_detail.html', {'book': book})
```

---

## Step 6: Create URL Patterns

In `myapp/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('<int:pk>/update/', views.book_update, name='book_update'),
    path('<int:pk>/delete/', views.book_delete, name='book_delete'),
]
```

Include your app URLs in `myproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('myapp.urls')),
]
```

---

## Step 7: Create Templates

Create a `templates/myapp` folder in your app directory.

**book_list.html**

```html
<h1>Books</h1>
<a href="{% url 'book_create' %}">Add New Book</a>
<ul>
  {% for book in books %}
    <li>
      <a href="{% url 'book_detail' book.pk %}">{{ book.title }}</a> |
      <a href="{% url 'book_update' book.pk %}">Edit</a> |
      <a href="{% url 'book_delete' book.pk %}">Delete</a>
    </li>
  {% endfor %}
</ul>
```

**book_form.html**

```html
<h1>{{ form.instance.pk|yesno:"Edit Book,Add Book" }}</h1>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>
<a href="{% url 'book_list' %}">Back to list</a>
```

**book_detail.html**

```html
<h1>{{ book.title }}</h1>
<p><strong>Author:</strong> {{ book.author }}</p>
<p><strong>Published Date:</strong> {{ book.published_date }}</p>
<p><strong>ISBN:</strong> {{ book.isbn }}</p>
<a href="{% url 'book_update' book.pk %}">Edit</a> |
<a href="{% url 'book_delete' book.pk %}">Delete</a> |
<a href="{% url 'book_list' %}">Back to list</a>
```

**book_confirm_delete.html**

```html
<h1>Delete Book</h1>
<p>Are you sure you want to delete "{{ book.title }}"?</p>
<form method="post">
  {% csrf_token %}
  <button type="submit">Confirm</button>
</form>
<a href="{% url 'book_list' %}">Cancel</a>
```

---

## Step 8: Run the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/books/](http://127.0.0.1:8000/books/) to see your CRUDL app in action!

---

## Summary

You’ve built a Django CRUDL application using:

* **Models** to define your data structure.
* **Forms** to create and update objects.
* **Views** to handle business logic.
* **Templates** for displaying the data.

You can now extend this app with features like search, filtering, and user authentication.

```


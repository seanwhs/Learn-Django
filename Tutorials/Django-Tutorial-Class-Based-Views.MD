<!-- Django-Tutorial-Class-Based-Views.MD -->
# Django CRUDL Tutorial Using Class-Based Views (CBVs)

This tutorial demonstrates how to create a Django CRUDL (Create, Read, Update, Delete, List) application using **Class-Based Views (CBVs)**, Django Models, and Django Forms.

---

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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'myapp',
]
```

---

## Step 3: Create a Model

In `myapp/models.py`:

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

## Step 4: Create a ModelForm

In `myapp/forms.py`:

```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn']
```

---

## Step 5: Create Class-Based Views

In `myapp/views.py`:

```python
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book
from .forms import BookForm

# List all books
class BookListView(ListView):
    model = Book
    template_name = 'myapp/book_list.html'
    context_object_name = 'books'

# View book details
class BookDetailView(DetailView):
    model = Book
    template_name = 'myapp/book_detail.html'
    context_object_name = 'book'

# Create a new book
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'myapp/book_form.html'
    success_url = reverse_lazy('book_list')

# Update a book
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'myapp/book_form.html'
    success_url = reverse_lazy('book_list')

# Delete a book
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'myapp/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
```

---

## Step 6: Configure URLs

In `myapp/urls.py`:

```python
from django.urls import path
from .views import (
    BookListView, BookDetailView, BookCreateView,
    BookUpdateView, BookDeleteView
)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
]
```

Include app URLs in `myproject/urls.py`:

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

Create a folder `templates/myapp` in your app directory.

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
<h1>{{ view.object.pk|yesno:"Edit Book,Add Book" }}</h1>
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

## Step 8: Run the Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/books/](http://127.0.0.1:8000/books/) to see your CRUDL application in action!

---

## Summary

You’ve built a Django CRUDL app using:

* **Models** to define your data structure.
* **ModelForms** for creating and updating data.
* **Class-Based Views** (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`) to handle logic.
* **Templates** to display the data.

This structure makes it easier to maintain and extend your app in the future.
# Django CRUDL Tutorial: Function-Based Views vs Class-Based Views

This tutorial demonstrates how to create a Django CRUDL (Create, Read, Update, Delete, List) application using **both Function-Based Views (FBVs) and Class-Based Views (CBVs)**. You can follow either approach to build your app.

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

## Step 5: Create Views

### 5a: Function-Based Views (FBVs)

In `myapp/views.py`:

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'myapp/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'myapp/book_detail.html', {'book': book})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'myapp/book_form.html', {'form': form})

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

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'myapp/book_confirm_delete.html', {'book': book})
```

---

### 5b: Class-Based Views (CBVs)

In `myapp/views.py` (alternative):

```python
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book
from .forms import BookForm

class BookListView(ListView):
    model = Book
    template_name = 'myapp/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'myapp/book_detail.html'
    context_object_name = 'book'

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'myapp/book_form.html'
    success_url = reverse_lazy('book_list')

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'myapp/book_form.html'
    success_url = reverse_lazy('book_list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'myapp/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
```

---

## Step 6: Configure URLs

### FBVs (`myapp/urls.py`):

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

### CBVs (`myapp/urls.py`):

```python
from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
]
```

Include app URLs in `myproject/urls.py` (common for both):

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

Create `templates/myapp/` folder. Templates are the same for both FBV and CBV.

* **book_list.html**
* **book_form.html**
* **book_detail.html**
* **book_confirm_delete.html**

> See individual FBV or CBV tutorial for full HTML code.

---

## Step 8: Run the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/books/](http://127.0.0.1:8000/books/) to see your CRUDL app in action.

---

## Summary

| Feature         | FBV                    | CBV                                         |
| --------------- | ---------------------- | ------------------------------------------- |
| Listing items   | `book_list` function   | `BookListView` class                        |
| Viewing details | `book_detail` function | `BookDetailView` class                      |
| Creating        | `book_create` function | `BookCreateView` class                      |
| Updating        | `book_update` function | `BookUpdateView` class                      |
| Deleting        | `book_delete` function | `BookDeleteView` class                      |
| Pros            | Simple, explicit       | Less boilerplate, reusable, scalable        |
| Cons            | More repetitive code   | Slightly harder to understand for beginners |



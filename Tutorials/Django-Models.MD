# 🌐 **Django Models Tutorial (Improved Version)**

Django **Models** define the structure of your database tables.
Each model corresponds to a **table**, and every model field represents a **column** in that table.

Models are the backbone of Django's MVT architecture, handling all data storage and retrieval.

---

# 📌 **1. What Is a Django Model?**

A Django model:

* represents a database table
* defines the table’s fields (columns)
* gives you a powerful Python ORM for CRUD operations
* lives inside an app’s `models.py` file

Basic example:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published = models.DateField()
```

---

# 📌 **2. Creating Your First Model**

Create an app:

```bash
python manage.py startapp library
```

Define a model in `library/models.py`:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    published_at = models.DateField()
```

---

# 📌 **3. Add App to INSTALLED_APPS**

Django must know about your app:

```python
INSTALLED_APPS = [
    ...
    'library',
]
```

---

# 📌 **4. Run Migrations**

Migrations turn your model code into actual database tables.

### Create migration files:

```bash
python manage.py makemigrations
```

### Apply them:

```bash
python manage.py migrate
```

---

# 📌 **5. Common Django Field Types**

### Text Fields

| Field                       | Use        |
| --------------------------- | ---------- |
| `CharField(max_length=...)` | Short text |
| `TextField()`               | Long text  |

### Numbers

| Field                                          | Use                                   |
| ---------------------------------------------- | ------------------------------------- |
| `IntegerField()`                               | Whole numbers                         |
| `FloatField()`                                 | Floating-point numbers                |
| `DecimalField(max_digits=?, decimal_places=?)` | Precise decimal values (e.g., prices) |

### Dates & Times

| Field               | Use                           |
| ------------------- | ----------------------------- |
| `DateField()`       | Date                          |
| `DateTimeField()`   | Date + time                   |
| `auto_now_add=True` | Automatically set on creation |
| `auto_now=True`     | Automatically updated on save |

### Files & Images

| Field          | Use                             |
| -------------- | ------------------------------- |
| `FileField()`  | Upload files                    |
| `ImageField()` | Upload images (requires Pillow) |

### Boolean

```python
active = models.BooleanField(default=True)
```

---

# 📌 **6. Relationships Between Models**

Django supports three relationship types:

---

### 1️⃣ **One-to-Many — `ForeignKey`**

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
```

---

### 2️⃣ **Many-to-Many — `ManyToManyField`**

```python
class Student(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
```

---

### 3️⃣ **One-to-One — `OneToOneField`**

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
```

---

# 📌 **7. Using the Django ORM (Queries)**

Open the Django shell:

```bash
python manage.py shell
```

### Create objects

```python
from library.models import Book
b = Book.objects.create(
    title="Django 101",
    author="Alice",
    pages=200,
    published_at="2024-01-01"
)
```

### Retrieve all

```python
Book.objects.all()
```

### Filter

```python
Book.objects.filter(author="Alice")
```

### Get one

```python
Book.objects.get(id=1)
```

### Update

```python
b = Book.objects.get(id=1)
b.pages = 250
b.save()
```

### Delete

```python
b.delete()
```

---

# 📌 **8. Model Meta Options**

Customize model behavior with an inner `Meta` class:

```python
class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)

    class Meta:
        ordering = ['title']
        verbose_name = "Library Book"
```

Common options:

| Option                | Purpose             |
| --------------------- | ------------------- |
| `ordering`            | Default sort order  |
| `verbose_name`        | Human-friendly name |
| `verbose_name_plural` | Plural display name |
| `db_table`            | Custom table name   |

---

# 📌 **9. Model Methods**

You can add custom behavior inside your model.

```python
class Book(models.Model):
    title = models.CharField(max_length=150)
    pages = models.IntegerField()

    def __str__(self):
        return self.title

    def is_long(self):
        return self.pages > 300
```

---

# 📌 **10. `get_absolute_url()` (Super Useful)**

Lets Django know where to redirect after saving.

```python
from django.urls import reverse

class Book(models.Model):
    title = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse("book_detail", args=[self.id])
```

---

# 📌 **11. Admin Integration**

Register your model so it appears in Django Admin.

`library/admin.py`:

```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Visit:

```
http://127.0.0.1:8000/admin/
```

---

# 📌 **12. Best Practices for Django Models**

✔ Always define `__str__()`
✔ Use `related_name` on relationships
✔ Keep models small and focused
✔ Use `choices=` for limited options
✔ Avoid `null=True` on string fields unless necessary
✔ Use `auto_now_add` and `auto_now` intentionally
✔ Write custom model methods to keep business logic in the model layer

---

# 🎉 **You Now Understand Django Models!**

You've learned:

✅ How to create models
✅ How migrations work
✅ Common field types
✅ Model relationships
✅ Querying using the ORM
✅ Meta options and model methods
✅ Admin integration


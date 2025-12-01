# 🌐 **Django MVT Tutorial**

Django is a powerful Python web framework built around the **MVT architecture**:

* **Model** → Defines and manages data structures
* **View** → Contains business logic and communicates with the model and template
* **Template** → Handles how data is presented to the user

To learn how these parts work together, let’s build a simple **Notes App**.

---

# ✅ **1. Install Django & Create a Project**

### Install Django

```bash
pip install django
```

### Create a new project

```bash
django-admin startproject mysite
cd mysite
```

### Start the development server

```bash
python manage.py runserver
```

Open your browser and visit:

**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

# ✅ **2. Create a Django App**

Inside your project folder, create a new app called **notes**:

```bash
python manage.py startapp notes
```

Then enable it in `mysite/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'notes',
]
```

---

# ✅ **3. Define the Model (M in MVT)**

Create a simple model to store notes.

`notes/models.py`

```python
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# ✅ **4. Create the View (V in MVT)**

The view retrieves all notes from the database and passes them to a template.

`notes/views.py`

```python
from django.shortcuts import render
from .models import Note

def notes_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/notes_list.html', {'notes': notes})
```

This view:

* pulls data from the **Model**
* sends that data to a **Template**

---

# ✅ **5. Create the Template (T in MVT)**

Create this folder structure:

```
notes/
    templates/
        notes/
            notes_list.html
```

`notes_list.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Notes</title>
</head>
<body>
    <h1>All Notes</h1>

    <ul>
        {% for note in notes %}
            <li>
                <strong>{{ note.title }}</strong><br>
                {{ note.content }}<br>
                <small>{{ note.created_at }}</small>
            </li>
            <hr>
        {% empty %}
            <p>No notes available.</p>
        {% endfor %}
    </ul>
</body>
</html>
```

---

# ✅ **6. Add URLs**

Tell Django which URL should display the notes list.

### In the main project file: `mysite/urls.py`

```python
from django.contrib import admin
from django.urls import path
from notes.views import notes_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', notes_list),
]
```

Visit:

**[http://127.0.0.1:8000/notes/](http://127.0.0.1:8000/notes/)**

---

# 🎉 **Your First MVT App is Ready!**

When you open `/notes`:

* the **View** retrieves note data
* the **Model** provides the data
* the **Template** renders it into HTML

You've just built a working Django app using the MVT architecture.



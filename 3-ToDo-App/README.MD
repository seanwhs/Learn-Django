# Todo Django Project

A simple **Todo application** built with **Django 5.2**, allowing users to manage tasks, set priorities, assign categories, and track due dates. Includes validation to ensure due dates are today or in the future and automated tests for models, forms, and views.

---

## Table of Contents

* [Features](#features)
* [Project Structure](#project-structure)
* [Setup & Installation](#setup--installation)
* [Models](#models)
* [Forms](#forms)
* [Views & URLs](#views--urls)
* [Templates](#templates)
* [Admin Panel](#admin-panel)
* [Testing](#testing)
* [License](#license)

---

## Features

* Create, update, delete, and list tasks
* Assign tasks to categories
* Set task priority: High, Medium, Low
* Set due date (cannot be in the past)
* Mark tasks as done
* Add new categories dynamically
* Fully tested with unit and integration tests

---

## Project Structure

```
Todo_Main/
│
├─ todo/                  # Main app for task management
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  └─ templates/task/
│      ├─ base.html
│      ├─ task_form.html
│      ├─ task_list.html
│      └─ task_delete.html
│
├─ category/              # App for task categories
│  ├─ admin.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ views.py
│  ├─ urls.py
│  └─ templates/category/
│      └─ category_form.html
│
├─ Todo_Main/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
│
└─ db.sqlite3
```

---

## Setup & Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd Todo_Main
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install django
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Access the app at: `http://127.0.0.1:8000/`

---

## Models

### `Category`

* Represents a task category (e.g., Work, Personal)
* Fields: `title`
* Admin: listed alphabetically, plural as **Categories**

### `Task`

* Represents a task with:
  * `category` → ForeignKey to `Category`
  * `title`, `description`, `is_done`
  * `priority` → High, Medium, Low
  * `due_date` → validated not to be in the past
  * Timestamps: `created_at`, `updated_at`
* Model validation ensures `due_date >= today`

---

## Forms

### `TaskForm`

* ModelForm for creating/updating tasks
* Fields: `category`, `priority`, `due_date`, `title`, `description`, `is_done`
* Uses Django's form validation; model `clean()` enforces due date rules

### `CategoryForm`

* ModelForm for adding new categories
* Fields: `title`
* Simple input placeholder: `"New Category"`

---

## Views & URLs

### Todo App Views

* `list_tasks` → shows all tasks
* `create_task` → create new task
* `update_task` → edit existing task
* `delete_task` → confirm and delete task

All views use **TaskForm** and enforce model validation with `full_clean()` before saving.

### Category App Views

* `create_category` → add a new category dynamically via `CategoryForm`
* Redirects to task list after creation

### Todo App URLs (`todo/urls.py`)

```python
urlpatterns = [
    path('', list_tasks, name='list'),
    path('create/', create_task, name='create'),
    path('update/<int:id>/', update_task, name='update'),
    path('delete/<int:id>/', delete_task, name='delete'),
]
```

### Category App URLs (`category/urls.py`)

```python
from django.urls import path
from .views import create_category

urlpatterns = [
    path('create/', create_category, name='create_category'),
]
```

### Main Project URLs (`Todo_Main/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('category', include('category.urls')),
]
```

---

## Templates

* **base.html** → base layout including header, nav, footer, and date/time display

### Navigation Menu

```html
<nav style="background-color:#f0f0f0; padding:10px; display:flex; gap:15px;">
    <a href="{% url 'list' %}">🏠 Home</a>
    <a href="{% url 'create' %}">➕ Add Task</a>
    <a href="{% url 'create_category' %}">🗂 Add Category</a>
</nav>
<hr>
```

* **task_list.html** → lists tasks with edit/delete links
* **task_form.html** → create/update task form
* **task_delete.html** → delete confirmation
* **category_form.html** → add category form

Uses Django template inheritance and `{% block %}` sections.

---

## Admin Panel

* `Category` and `Task` registered in admin.
* TaskAdmin includes:
  * List display: title, priority, due_date, is_done, timestamps
  * Filters: category, is_done
  * Search: title, description

---

## Testing

Located in `todo/tests.py`:

* **Model Tests**: task creation, due date validation, `__str__`
* **Form Tests**: validation and model `full_clean()` enforcement
* **View Tests**: task listing, creation, updating, deletion

Run tests:

```bash
python manage.py test todo
```

---

## License

MIT License – free to use and modify.

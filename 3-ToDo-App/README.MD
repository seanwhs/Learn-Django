# Todo Django Project

A simple **Todo application** built with **Django 5.2**, allowing users to manage tasks, organize categories, set priorities, and track due dates.  
Now includes **Automatic Overdue Detection**, which highlights overdue tasks and displays a warning banner when tasks are past their due dates.

---

## Table of Contents

* [Features](#features)
* [Automatic Overdue Detection](#automatic-overdue-detection)
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
* Set priority: High, Medium, Low
* Set due dates (validated not to be in the past)
* Mark tasks as done
* Add categories dynamically
* **Automatic overdue detection with visual alerts**
* Fully tested with unit and integration tests

---

## Automatic Overdue Detection

This feature automatically identifies tasks that are overdue based on today's date.

### How It Works

1. Each task has a method `is_overdue()` that checks:
   - Task has a due date  
   - Due date is before today  
   - Task is **not done**  
   - Task is **not recurring**  

2. Your `list_tasks` view counts overdue tasks and exposes that number to the template.

3. The `task_list.html` template:
   - Highlights overdue tasks with a red border  
   - Shows a warning alert inside each overdue task  
   - Displays a top banner:  
     **⚠️ You have X overdue tasks!**

4. Optional CSS improves the visibility of overdue tasks.

---

## Project Structure

```

Todo_Main/
│
├─ todo/
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
├─ category/
│  ├─ admin.py
│  ├─ forms.py
│  ├─ models.py
│  ├─ urls.py
│  ├─ views.py
│  └─ templates/category/
│      └─ category_form.html
│
├─ Todo_Main/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
│
└─ db.sqlite3

````

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd Todo_Main
````

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install django
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Models

### Category Model

* Includes a normalized `title` field (`strip()` + `title()`)
* Prevents duplicate category names
* Used to group tasks

### Task Model

* Fields:

  * `category`
  * `title`, `description`
  * `priority`
  * `due_date`
  * `is_done`
  * `recurrence`
  * timestamps

* Validates:

  * One-time tasks must have a due date
  * Due dates cannot be in the past
  * Recurring tasks cannot be marked done

### Overdue Logic

```python
def is_overdue(self):
    return (
        self.due_date is not None
        and self.due_date < date.today()
        and not self.is_done
        and not self.recurrence
    )
```

---

## Forms

### TaskForm

* HTML5 date picker (`type="date"`)
* Applies model validation
* Fields: category, title, description, priority, due_date, recurrence, is_done

### CategoryForm

* Normalizes title input
* Prevents duplicates
* Used for adding categories directly from the UI

---

## Views & URLs

### Todo App Views

* `list_tasks` — Shows all tasks + overdue count
* `create_task` — Add a task
* `update_task` — Edit a task
* `delete_task` — Delete a task with confirmation

### Category App Views

* Create, update, delete categories
* Uses custom validation to prevent duplicates

---

### Todo URLs (`todo/urls.py`)

```python
urlpatterns = [
    path('', list_tasks, name='list'),
    path('create/', create_task, name='create'),
    path('update/<int:id>/', update_task, name='update'),
    path('delete/<int:id>/', delete_task, name='delete'),
]
```

### Category URLs (`category/urls.py`)

```python
urlpatterns = [
    path('create/', create_category, name='create_category'),
    path('update/<int:id>/', update_category, name='update_category'),
    path('delete/<int:id>/', delete_category, name='delete_category'),
]
```

### Main Project URLs (`Todo_Main/urls.py`)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    path('category/', include('category.urls')),
]
```

---

## Templates

### base.html

* Contains navigation layout and shared structure.

### task_list.html

Now supports:

**Overdue banner:**

```html
{% if overdue_count > 0 %}
<div class="alert alert-warning">
    ⚠️ You have {{ overdue_count }} overdue task{{ overdue_count|pluralize }}!
</div>
{% endif %}
```

**Overdue highlighting:**

```html
<li class="{% if task.is_overdue %}overdue{% endif %}">
```

### task_form.html

* Displays form for creating/updating tasks

### task_delete.html

* Confirmation page for deletion

### category_form.html

* Add/update categories

---

## Admin Panel

* Both Task and Category models are fully registered.
* Admin features:

  * List display for tasks
  * Filters for status and category
  * Search fields
  * Automatic ordering

---

## Testing

Stored in `todo/tests.py`.

Tests include:

* Model tests (validation, overdue logic)
* Form tests
* View/URL tests
* Template rendering tests

Run tests:

```bash
python manage.py test
```

---

## License

MIT License — free to use, modify, and distribute.

```



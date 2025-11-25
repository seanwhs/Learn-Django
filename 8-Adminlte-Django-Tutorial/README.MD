# AdminLTE + Django Tutorial

## Table of Contents — Tutorial

1. [Create Project Environment](#1---create-project-environment)
2. [Install Django & django-adminlte3](#2---install-django--django-adminlte3)
3. [Create a New Django Project and App](#3---create-a-new-django-project-and-app)
4. [Create a Superuser](#4---create-a-superuser)
5. [Enable django-adminlte3 Templates](#5---enable-django-adminlte3-templates)
6. [Create a Simple View Using AdminLTE Base Template](#6---create-a-simple-view-using-adminlte-base-template)
7. [Add URL Routing](#7---add-url-routing)
8. [How Template Inheritance Works](#8---how-template-inheritance-works)
9. [Override the Sidebar](#9---override-the-sidebar)
10. [Override Header and Footer](#10---override-header-and-footer)
11. [How Header, Sidebar, Content, Footer Fit Together](#11---how-header-sidebar-content-footer-fit-together)
12. [High-Level Template Flow](#12---high-level-template-flow)
13. [Visual Diagram of AdminLTE Layout](#13---visual-diagram-of-adminlte-layout)

## Table of Contents — Optional Sections A → Z

A. [Cards, Tables, and Forms](#a---cards-tables-and-forms)
B. [Custom Top-Right User Menu](#b---custom-top-right-user-menu)
C. [Dashboard with Charts (Chart.js)](#c---dashboard-with-charts-chartjs)
D. [Custom Base Template](#d---custom-base-template)
E. [Alerts & Django Messages](#e---alerts--django-messages)
F. [Modals (Pop-ups)](#f---modals-pop-ups)
G. [Buttons & UI Components](#g---buttons--ui-components)
H. [Form Validation Styling](#h---form-validation-styling)
I. [Sidebar Collapsible Menu (Treeview)](#i---sidebar-collapsible-menu-treeview)
J. [DataTables Integration](#j---datatables-integration)
K. [Layout Options](#k---layout-options)
L. [FontAwesome Pro / Icon Packs](#l---fontawesome-pro--icon-packs)
M. [Reusable Components (`{% include %}`)](#m---reusable-components-include)
N. [Toast Notifications (SweetAlert2 + Toastr)](#n---toast-notifications-sweetalert2--toastr)
O. [Widgets: Info Boxes, Small Boxes, Stat Cards](#o---widgets-info-boxes-small-boxes-stat-cards)
P. [Timeline Component](#p---timeline-component)
Q. [Mailbox UI and Chat UI](#q---mailbox-ui-and-chat-ui)
R. [Kanban Board Integration](#r---kanban-board-integration)
S. [File Uploads with Preview (bs-custom-file-input)](#s---file-uploads-with-preview-bs-custom-file-input)
T. [Pace Loader (AJAX Progress Bar)](#t---pace-loader-ajax-progress-bar)
U. [Control Sidebar (Right Sidebar Panel)](#u---control-sidebar-right-sidebar-panel)
V. [AdminLTE Plugins (Select2, Summernote, DateRangePicker)](#v---adminlte-plugins-select2-summernote-daterangepicker)
W. [Dynamic Sidebar Using Database Menus](#w---dynamic-sidebar-using-database-menus)
X. [CRUD UI (Create, Edit, Delete)](#x---crud-ui-create-edit-delete)
Y. [Django REST Framework Integration](#y---django-rest-framework-integration)
Z. [Deployment with Nginx + Gunicorn](#z---deployment-with-nginx--gunicorn)

---

## 1 — Create Project Environment

```bash
virtualenv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

## 2 — Install Django & django-adminlte3

```bash
pip install django django-adminlte3
pip install django-adminlte3-admin  # Optional for Admin styling
```

## 3 — Create a New Django Project and App

```bash
django-admin startproject DemoAdminLTE3 .
python manage.py startapp DemoApp
python manage.py makemigrations
python manage.py migrate
```

## 4 — Create a Superuser

```bash
python manage.py createsuperuser
python manage.py runserver
```

Visit:

* App root → [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Admin → [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 5 — Enable django-adminlte3 Templates

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'DemoApp',
    
    'adminlte3',
    'adminlte3_theme',
]

TEMPLATES = [
    {
        'DIRS': [BASE_DIR / "templates"],   # Important
        ...
    }
]
```

---

## 6 — Create a Simple View Using AdminLTE Base Template

**`DemoApp/templates/demoapp/home.html`**

```django
{% extends "adminlte/base.html" %}

{% block content %}
<div class="container">
    <h1 class="mt-4">Welcome to AdminLTE Demo</h1>
    <p>This page uses the AdminLTE3 layout!</p>
</div>
{% endblock %}
```

**`DemoApp/views.py`**

```python
from django.shortcuts import render

def home(request):
    return render(request, 'demoapp/home.html')
```

---

## 7 — Add URL Routing

**`DemoApp/urls.py`**

```python
from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),
]
```

**`DemoAdminLTE3/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DemoApp.urls')),
]
```

---

## 8 — How Template Inheritance Works

```
home.html
  ↓ extends
adminlte/base.html
  ↓ includes
_main_header.html
_main_sidebar.html
_main_footer.html
```

*Tip:* You can override any AdminLTE template by recreating its folder structure in `templates/`.

---

## 9 — Override the Sidebar

Original template:

```
adminlte3/templates/adminlte/lib/_main_sidebar.html
```

Override location in your project:

```
project_root/
    templates/
        adminlte/
            lib/
                _main_sidebar.html
```

Supports nested blocks: `logo`, `user_panel`, `nav_links`.

---

## 10 — Override Header and Footer

Create:

```
templates/adminlte/lib/_main_header.html
templates/adminlte/lib/_main_footer.html
```

Add navigation links, user profile, and footer content.

---

## 11 — How Header, Sidebar, Content, Footer Fit Together

```django
<div class="wrapper">
    {% block main_header %}{% endblock %}
    {% block main_sidebar %}{% endblock %}
    <div class="content-wrapper">{% block content %}{% endblock %}</div>
    {% block main_footer %}{% endblock %}
</div>
```

---

## 12 — High-Level Template Flow

```
home.html
  ↓ extends
adminlte/base.html
  ↓ injects
_main_header.html
_main_sidebar.html
_main_footer.html
```

---

## 13 — Visual Diagram of AdminLTE Layout

```
┌───────────────────────────────────────────────┐
│                  MAIN HEADER                  │
└───────────────────────────────────────────────┘

┌───────────────┬───────────────────────────────┐
│   SIDEBAR     │       CONTENT WRAPPER         │
└───────────────┴───────────────────────────────┘

┌───────────────────────────────────────────────┐
│                  MAIN FOOTER                  │
└───────────────────────────────────────────────┘
```

---

## Optional Sections A-Z

### A — Cards, Tables, and Forms

```django
<div class="card card-primary">
  <div class="card-header">Title</div>
  <div class="card-body">
    Card content here
  </div>
</div>
```

**Tip:** Use `.card-outline` for border-only cards and `.card-success`/`.card-danger` for colored cards.

---

### B — Custom Top-Right User Menu

```django
<ul class="navbar-nav ml-auto">
  <li class="nav-item dropdown">
    <a class="nav-link" data-toggle="dropdown" href="#">User</a>
    <div class="dropdown-menu dropdown-menu-right">
      <a href="/profile" class="dropdown-item">Profile</a>
      <a href="/logout" class="dropdown-item">Logout</a>
    </div>
  </li>
</ul>
```

**Tip:** Use `request.user` in Django to dynamically show the logged-in username.

---

### C — Dashboard with Charts (Chart.js)

```django
<canvas id="myChart"></canvas>
<script>
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar'],
        datasets: [{ label: 'Sales', data: [10, 20, 30] }]
    }
});
</script>
```

**Tip:** Include Chart.js via CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

---

### D — Custom Base Template

```django
{% extends "adminlte/base.html" %}

{% block main_header %}
<!-- Custom header -->
{% endblock %}

{% block main_sidebar %}
<!-- Custom sidebar -->
{% endblock %}

{% block content %}
<!-- Custom content -->
{% endblock %}

{% block main_footer %}
<!-- Custom footer -->
{% endblock %}
```

**Tip:** This is useful for defining a project-wide layout while still leveraging AdminLTE.

---

### E — Alerts & Django Messages

```django
{% if messages %}
  {% for message in messages %}
    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
      {{ message }}
      <button type="button" class="close" data-dismiss="alert">&times;</button>
    </div>
  {% endfor %}
{% endif %}
```

**Tip:** AdminLTE supports `alert-success`, `alert-danger`, `alert-warning`, etc., corresponding to Django message tags.

---

### F — Modals (Pop-ups)

```django
<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
  Launch Modal
</button>

<div class="modal fade" id="exampleModal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Modal Title</h5>
        <button type="button" class="close" data-dismiss="modal">&times;</button>
      </div>
      <div class="modal-body">
        Modal body content here
      </div>
    </div>
  </div>
</div>
```

**Tip:** Use modals for confirmation dialogs, forms, or displaying details without page reloads.

---

### G — Buttons & UI Components

```django
<button class="btn btn-success">Success Button</button>
<button class="btn btn-danger">Danger Button</button>
<div class="badge badge-primary">Badge</div>
```

**Tip:** AdminLTE also provides `.btn-flat`, `.btn-block`, `.btn-sm`, and `.btn-lg` for more UI variations.

---

### H — Form Validation Styling

```django
<form method="post">
  {% csrf_token %}
  <div class="form-group">
    <input type="text" class="form-control {% if form.name.errors %}is-invalid{% endif %}" name="name">
    <div class="invalid-feedback">{{ form.name.errors }}</div>
  </div>
</form>
```

**Tip:** Use `.is-valid` and `.is-invalid` for real-time validation feedback.

---

### I — Sidebar Collapsible Menu (Treeview)

```django
<li class="nav-item has-treeview">
  <a href="#" class="nav-link">
    <p>
      Menu
      <i class="right fas fa-angle-left"></i>
    </p>
  </a>
  <ul class="nav nav-treeview">
    <li class="nav-item"><a href="#" class="nav-link">Submenu 1</a></li>
    <li class="nav-item"><a href="#" class="nav-link">Submenu 2</a></li>
  </ul>
</li>
```

**Tip:** Use `menu-open` class on parent `<li>` to expand by default.

---

### J — DataTables Integration

```django
<table id="example1" class="table table-bordered table-striped">
  <thead>
    <tr><th>Name</th><th>Age</th></tr>
  </thead>
  <tbody>
    <tr><td>John</td><td>30</td></tr>
  </tbody>
</table>

<script>
$(function () {
  $("#example1").DataTable();
});
</script>
```

**Tip:** Include DataTables CSS & JS via CDN for quick setup:

```html
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
```

---

### K — Layout Options

* Fixed sidebar/navbar: `layout-fixed`
* Dark mode: `dark-mode`
* Sidebar collapse: `sidebar-collapse`
* Boxed layout: `layout-boxed`

**Tip:** Add these classes to the `<body>` tag in `base.html` for instant layout changes.

---

### L — FontAwesome Pro / Icon Packs

```html
<script src="https://kit.fontawesome.com/your-kit-code.js" crossorigin="anonymous"></script>
```

```django
<i class="fas fa-user"></i> Profile
```

**Tip:** Free FontAwesome icons also work with AdminLTE.

---

### M — Reusable Components (`{% include %}`)

```django
<!-- templates/includes/navbar.html -->
<nav>Navbar Content</nav>
```

```django
{% include 'includes/navbar.html' %}
```

**Tip:** Great for DRY layouts with repeated headers, footers, or cards.

---

### N — Toast Notifications (SweetAlert2 + Toastr)

```django
<script>
toastr.success('Data saved successfully!');
</script>
```

**Tip:** Include Toastr JS & CSS via CDN:

```html
<link href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
```

---

### O — Widgets: Info Boxes, Small Boxes, Stat Cards

```django
<div class="small-box bg-info">
  <div class="inner"><h3>150</h3><p>New Orders</p></div>
  <div class="icon"><i class="ion ion-bag"></i></div>
</div>
```

**Tip:** Change `bg-info` to `bg-success`, `bg-warning`, or `bg-danger` for color variations.

---

### P — Timeline Component

```django
<div class="timeline">
  <div class="time-label"><span class="bg-red">10 Feb. 2025</span></div>
  <div>
    <i class="fas fa-envelope bg-blue"></i>
    <div class="timeline-item">
      <h3 class="timeline-header">Event Title</h3>
    </div>
  </div>
</div>
```

**Tip:** Use timeline for activity logs, notifications, or history feeds.

---

### Q — Mailbox UI and Chat UI

**Mailbox:**

```django
<a href="#" class="mailbox-read-message">Message Title</a>
```

**Chat:**

```django
<div class="direct-chat-msg">
  <div class="direct-chat-text">Hello!</div>
</div>
```

**Tip:** Combine with AdminLTE chat widgets for live messaging interfaces.

---

### R — Kanban Board Integration

```django
<div class="kanban-column">
  <div class="card">Task 1</div>
  <div class="card">Task 2</div>
</div>
```

**Tip:** Use drag-and-drop libraries like `Sortable.js` for full Kanban functionality.

---

### S — File Uploads with Preview (bs-custom-file-input)

```django
<div class="custom-file">
  <input type="file" class="custom-file-input" id="customFile">
  <label class="custom-file-label" for="customFile">Choose file</label>
</div>
<script>bsCustomFileInput.init();</script>
```

**Tip:** Initialize `bsCustomFileInput` after DOM load for multiple file inputs.

---

### T — Pace Loader (AJAX Progress Bar)

```django
<script src="plugins/pace/pace.min.js"></script>
<link rel="stylesheet" href="plugins/pace/pace-theme-minimal.css">
```

**Tip:** Shows a progress bar for AJAX requests and page loads automatically.

---

### U — Control Sidebar (Right Sidebar Panel)

```django
<aside class="control-sidebar control-sidebar-dark">
  <div class="p-3">Sidebar content</div>
</aside>
```

**Tip:** Toggle visibility via JavaScript:

```javascript
$('.control-sidebar').controlSidebar('toggle');
```

---

### V — AdminLTE Plugins (Select2, Summernote, DateRangePicker)

```django
<select class="select2" style="width:100%"></select>
<textarea class="summernote"></textarea>
<input type="text" class="daterangepicker">
```

**Tip:** Initialize plugins in JS:

```javascript
$('.select2').select2();
$('.summernote').summernote();
$('input.daterangepicker').daterangepicker();
```

---

### W — Dynamic Sidebar Using Database Menus

```python
# views.py
menus = Menu.objects.all()
return render(request, 'demoapp/home.html', {'menus': menus})
```

```django
{% for menu in menus %}
<li>{{ menu.title }}</li>
{% endfor %}
```

**Tip:** Allows dynamically generated menus based on user permissions.

---

### X — CRUD UI (Create, Edit, Delete)

```django
<a href="{% url 'edit' item.id %}" class="btn btn-sm btn-primary">Edit</a>
<a href="{% url 'delete' item.id %}" class="btn btn-sm btn-danger">Delete</a>
```

**Tip:** Combine with modals for inline editing to enhance UX.

---

### Y — Django REST Framework Integration

```bash
pip install djangorestframework
```

```python
# serializers.py
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
```

```python
# views.py
from rest_framework import viewsets

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

**Tip:** Combine with DRF routers to quickly generate API endpoints.

---

### Z — Deployment with Nginx + Gunicorn

```bash
gunicorn DemoAdminLTE3.wsgi:application --bind 0.0.0.0:8000
```

**Sample Nginx server block:**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Tip:** Use `systemd` to manage Gunicorn as a service for automatic restarts.






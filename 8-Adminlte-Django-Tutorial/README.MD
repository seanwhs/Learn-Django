# django-adminlte3 Tutorial

django-adminlte3 is a Python module which "provides the functionality of the AdminLTE3 theme to Django developers in the form of standard base templates. Optional styling for Django's built-in admin interface is also provided."

From https://pypi.org/project/django-adminlte3/

In short, it lets you make your Django projects look very pretty with a consistent looking UI for minimal effort. 

For documentation of the module, see https://django-adminlte2.readthedocs.io

## 1. Setup Project Environment

Create directory and virtual environment:

```bash
virtualenv venv
.venv\Scripts\activate      # Windows
```

## 2. Install Django and django-adminlte3

Inside your activated virtual environment:

```bash
pip install django django-adminlte3
```

(If you also want to style the built-in Django admin interface, you can additionally install `django-adminlte3-admin`.)


## 3. Create a New Django Project

```bash
django-admin startproject adminlte_demo .
```

Verify you're in the virtual environment by showing the installed pip modules
```
pip list
```

Create Django project (e.g., DemoAdminLTE3) and your app (e.g., DemoApp)

```
django-admin startproject DemoAdminLTE3 .
py .\manage.py startapp DemoApp

```

Run initial migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Test Project

Create superuser account (so you can access Django admin pages)
```
py manage.py createsuperuser

Username (leave blank to use 'sean'): admin
Email address: admin@email.com
Password: djangorocks
Password (again): djangorocks
```

Run server and access both landing and admin pages and see what the default looks like

```
py manage.py runserver
```


## 5. Add *django-adminlte3* to Installed Apps

Open **DemoAdminLTE3/settings.py** and add the following:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DemoApp',

    # AdminLTE
    'adminlte3',     # General use templates & template tags (should appear first before apps)
    'adminlte3_theme',  # optional: admin interface styling
]
```
Run server and access both landing and admin pages and see how AdminLTE3 affects your admin login page

## 6. Create a View Using the AdminLTE Base Template

Add DemoApp to settings.py

To get a taste for what AdminLTE3 can do, create a template page home.html in
DemoApp/templates/demoapp/

```
{% extends "adminlte/base.html" %}

{% block content %}
<div class="container">
    <h1 class="mt-4">Welcome to AdminLTE Demo</h1>
    <p>This page uses the AdminLTE3 layout!</p>
</div>
{% endblock %}

```

Create a view in DemoApp/views.py:

```
from django.shortcuts import render

def home(request):
    return render(request, 'demoapp/home.html')
```

## 7. Set Up URL Routing

Create and Edit DemoApp/urls.py:
```
from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),
]
```

include DemoApp.urls into the main urls.py
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DemoApp.urls')),
]

```

## 7. Create a View Using the AdminLTE Base Template

Make sure the app DemoApp has been added to settings.py


Create a view in **DemoApp/views.py**:

```python
from django.shortcuts import render

def home(request):
    return render(request, "home.html")
```


## 8. Create a Template That Extends AdminLTE

Create directory:

```
DemoApp/templates/demoapp/home.html
```

Add:

```html
{% extends "adminlte/base.html" %}

{% block content %}
<div class="container">
    <h1 class="mt-4">Welcome to AdminLTE Demo</h1>
    <p>This page uses the AdminLTE3 layout!</p>
</div>
{% endblock %}
```


### What's going on here?

- Just as with any Django templates, you're using Jinja2 formatting with the usual {% %} tags in your template file
- Line 1 extends the default AdminLTE base.html file included by the pip module, allowing you to override different blocks defined in that template. (This is typically the minimum you'll want to do.)
- The two blocks, title and content, which are defined in base.html, are overridden, resulting in their contents appearing on the page. These were chosen just to show how things fit together (think "hello world"). If you did not override these (i.e., if you deleted all but the first line), you'd see whatever was defined in the default AdminLTE template base.html file.

## 9. Set Up URL Routing

Edit **adminlte_demo/urls.py**:

```python
from django.contrib import admin
from django.urls import path
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]
```


## 10. Run the Development Server

```bash
python manage.py runserver
```

Open your browser at:

```
http://127.0.0.1:8000/
```

You should now see a beautiful AdminLTE-styled page.

### How Does This Work?

When you install the django-adminlte3 Python module using pip, it gets installed like any other Python module into the site-packages directory. For example, if you followed the steps above, take a look in

Django-AdminLTE3/lib/python<version>/site-packages

There you will find directories adminlte3, adminlte3_theme, django, and django_adminlte3, among others. adminlte3 contains the actual AdminLTE template files. Note you don't modify these. If you wish to customize things, you create your own versions, which you store in a path that matches the default ones (more on that in a minute). And in these you place an {% extend <file> %} line at the top to pull that default file in and then modify it as needed. But it's worth knowing where the default ones live in case you want to look at them. Either that or download the official AdminLTE files and look through those for examples to work with. To see examples of what the template offers, check out their live preview page.

## 11. Modifying the Sidebar

AdminLTE provides a flexible left sidebar that you can customize—logos, menu headings, links, icons, user panels, and dynamic active states.

We can override and modify the sidebar in a Django project using django-adminlte3.

## 12. Understand How django-adminlte3 Loads Templates

AdminLTE’s default sidebar template lives inside the package:

```
adminlte3/templates/adminlte/lib/_main_sidebar.html
```

Django automatically lets you override this file by creating a file in your project with the same path:

```
your_project/
    templates/
        adminlte/
            lib/
                _main_sidebar.html   ← this overrides the package version

```

This file is NOT used directly as a standalone template.
It is inserted automatically by the main layout:

```
adminlte/base.html
```

So your pages should extend:

```
{% extends "adminlte/base.html" %}
```

## 13. Create the Override File

Create the folder structure:
```
templates/
    adminlte/
        lib/
            _main_sidebar.html

```
## 14. Write Your Custom Sidebar Template

Paste this inside templates/adminlte/lib/_main_sidebar.html:
```
{% load static %}

{% block main_sidebar %}
<aside class="main-sidebar sidebar-dark-primary elevation-4">

    <!-- BRAND LOGO -->
    {% block logo %}
    <a href="/" class="brand-link">
        <img src="{% static 'DemoApp/logo.png' %}"
             alt="My Logo"
             class="brand-image img-circle elevation-3"
             style="opacity: 0.8;">
        <span class="brand-text font-weight-light">DemoApp</span>
    </a>
    {% endblock logo %}

    <!-- SIDEBAR -->
    <div class="sidebar">

        <!-- OPTIONAL USER PANEL -->
        {% block user_panel %}
        <!-- Remove or customize -->
        <div class="user-panel mt-3 pb-3 mb-3 d-flex">
            <div class="image">
                <img src="{% static 'adminlte/img/user2-160x160.jpg' %}"
                     class="img-circle elevation-2"
                     alt="User Image">
            </div>
            <div class="info">
                <a href="#" class="d-block">{{ request.user.username }}</a>
            </div>
        </div>
        {% endblock user_panel %}

        <!-- MENU HEADER -->
        <div class="nav-header">
            {% block nav_heading %}NAVIGATION{% endblock nav_heading %}
        </div>

        <!-- MENU LINKS -->
        <nav class="mt-2">
            <ul class="nav nav-pills nav-sidebar flex-column">

                {% block nav_links %}

                <!-- HOME LINK -->
                <li class="nav-item">
                    <a href="/" class="nav-link {% if request.path == '/' %}active{% endif %}">
                        <i class="nav-icon fas fa-home"></i>
                        <p>Home</p>
                    </a>
                </li>

                <!-- ADMIN -->
                <li class="nav-item">
                    <a href="/admin" class="nav-link">
                        <i class="nav-icon fas fa-cog"></i>
                        <p>Admin</p>
                    </a>
                </li>

                <!-- COLLAPSIBLE MENU EXAMPLE -->
                <li class="nav-item has-treeview">
                    <a href="#" class="nav-link">
                        <i class="nav-icon fas fa-folder"></i>
                        <p>
                            Sections
                            <i class="right fas fa-angle-left"></i>
                        </p>
                    </a>

                    <ul class="nav nav-treeview">
                        <li class="nav-item">
                            <a href="/section/a" class="nav-link">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Section A</p>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="/section/b" class="nav-link">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Section B</p>
                            </a>
                        </li>
                    </ul>
                </li>

                {% endblock nav_links %}
            </ul>
        </nav>

    </div>
</aside>
{% endblock main_sidebar %}

```

MAKE SURE TO ENABLE PROJECT LEVEL TEMPLATE DIRECTORY in settings.py:
```
TEMPLATES['DIRS'] # → project-level template directories
```

Sure! Here are similar points for your `_main_sidebar.html` template:

* AdminLTE3 uses the `main-sidebar` class for the sidebar.
* The template defines the main block `main_sidebar` that wraps the entire sidebar.
* Nested blocks allow fine-grained customization:

  * `logo` – for the brand logo at the top.
  * `user_panel` – for the user avatar and username section.
  * `nav_heading` – for the menu header text (e.g., "NAVIGATION").
  * `nav_links` – for the actual navigation links and submenus.
* You can override any of these blocks in child templates to add, remove, or modify content.
* Conditional classes (like `{% if request.path == '/' %}active{% endif %}`) allow highlighting the current page.
* Collapsible menus are supported using `.has-treeview` and nested `<ul>` elements.
* Static assets (images, icons) are referenced via `{% static %}` to ensure proper loading.

## 15.  Customize header and footer in django-adminlte

To customize the header and footer in the django-adminlte package, you should use Django's template inheritance system to override specific template blocks in your own project's template directory. The package is designed to allow you to redefine these blocks in your project without modifying the original package files. 

### Customizing the Header
The main header in django-adminlte can be customized by overriding the adminlte/lib/_main_header.html template or specific blocks within it. 

- Create the directory structure: In your project's templates folder, create the path adminlte/lib/.
- Create the template file: Inside the adminlte/lib/ folder, create a file named _main_header.html.
- Override the blocks: Copy the original content (if you want to keep most of it) or define your own custom content using the provided blocks within your new _main_header.html file. For finer control, you can override specific blocks like nav_header. 

### Customizing the Footer
- Similarly, the footer can be customized by overriding the adminlte/lib/_main_footer.html template or its specific blocks. 
- Create the directory structure: Ensure the adminlte/lib/ path exists in your project's templates folder.
- Create the template file: Inside the adminlte/lib/ folder, create a file named _main_footer.html.
- Override the blocks: Define your custom footer content here. The nav_footer block is available for customization. You can use the {% block nav_footer %} to place a custom message, copyright info, or links (e.g., &copy; 2025 My Company). 

### Using Template Inheritance
- In your custom template file, you would use Django template tags to manage the content. 
- To append to the existing content, use {{ block.super }} within your custom block.
- To entirely replace the content, simply define the block without calling {{ block.super }}. 

### Custom Header

File: templates/adminlte/lib/_main_header.html

```
{% load static %}

<!-- Main Header -->
<nav class="main-header navbar navbar-expand navbar-white navbar-light">

    <!-- Left navbar links -->
    <ul class="navbar-nav">
        <li class="nav-item">
            <a href="/" class="nav-link">Home</a>
        </li>
        <li class="nav-item">
            <a href="/about" class="nav-link">About</a>
        </li>
    </ul>

    <!-- Right navbar links -->
    <ul class="navbar-nav ml-auto">
        <li class="nav-item">
            <a href="/profile" class="nav-link">Profile</a>
        </li>
        <li class="nav-item">
            <a href="/logout" class="nav-link">Logout</a>
        </li>
    </ul>

</nav>
```

Here’s a summary for **header** and **footer** in a style similar to your sidebar points:

---

### Header (`_main_header.html`)

* AdminLTE3 uses the `main-header` class for the header/navbar.
* The template defines the main block `main_header` that wraps the entire top navigation.
* Nested blocks or sections allow customization of:

  * **Left navbar links** – for Home, About, or other pages.
  * **Right navbar links** – for user actions like Logout, profile, notifications.
* You can override `main_header` in your templates to add custom navigation, buttons, or branding.
* Supports Bootstrap navbar classes (`navbar-expand`, `navbar-light`, `navbar-white`) for styling.
* Static assets like logos or icons can be included via `{% static %}`.

### Custom Footer

- File: templates/adminlte/lib/_main_footer.html

```
{% load static %}

<footer class="main-footer">
    {% block footer_text %}
        <strong>&copy; 2025 DemoApp</strong> — All rights reserved.
    {% endblock footer_text %}

    <div class="float-right d-none d-sm-inline">
        {% block footer_version %}Version 1.0.0{% endblock footer_version %}
    </div>
</footer>
```

* AdminLTE3 uses the `main-footer` class for the footer section.
* The template defines the main block `main_footer` that wraps the footer content.
* Nested blocks allow fine-grained customization:

  * `footer_text` – for copyright or legal info.
  * `footer_version` – for application version or additional info.
* You can override these blocks in your templates to display custom messages, links, or HTML.
* The `float-right` class can be used to align version or extra info to the right.
* Supports including links, icons, or small scripts as part of the footer.


## 16. How it all works together

Summary showing **how header, sidebar, content, and footer work together** in AdminLTE3 with Django:


### AdminLTE3 Layout Structure in Django

```
< div class="wrapper" >

    <!-- HEADER -->
    {% block main_header %}
        <!-- _main_header.html content -->
    {% endblock %}

    <!-- SIDEBAR -->
    {% block main_sidebar %}
        <!-- _main_sidebar.html content -->
    {% endblock %}

    <!-- CONTENT -->
    <div class="content-wrapper">
        {% block content %}
            <!-- Page-specific content goes here -->
        {% endblock %}
    </div>

    <!-- FOOTER -->
    {% block main_footer %}
        <!-- _main_footer.html content -->
    {% endblock %}

< /div >
```
1. **Wrapper**

   * The `<div class="wrapper">` contains the entire page layout.
   * Header, sidebar, content, and footer are all children of this wrapper.

2. **Header (`main_header`)**

   * Top navbar area using `main-header` class.
   * Can include left and right links, logo, user menus.
   * Override `_main_header.html` in your project templates/adminlte/lib/ to customize.

3. **Sidebar (`main_sidebar`)**

   * Vertical navigation panel using `main-sidebar` class.
   * Typically includes logo, user panel, and navigation links.
   * Nested blocks allow you to override:

     * `logo` → brand logo and text
     * `user_panel` → user info and avatar
     * `nav_links` → menu items and collapsible sections

4. **Content (`content-wrapper`)**

   * Main page area where your Django views render content.
   * Use `{% block content %}` in each template for page-specific content.

5. **Footer (`main_footer`)**

   * Bottom section using `main-footer` class.
   * Can customize with nested blocks:

     * `footer_text` → copyright/legal info
     * `footer_version` → version or other info aligned to the right
   * Override `_main_footer.html` in your project templates/adminlte/lib/ to customize.


### Key Points

* **Template inheritance** is the core mechanism: each page template extends a base template (or `custom_base.html`).
* **Nested blocks** allow granular overrides without touching AdminLTE3 package files.
* **Static files** like logos and avatars are referenced via `{% static %}`.
* **Customizing a block** can either **replace** it entirely or **append** to it using `{{ block.super }}`.

## 17. Visual Diagram of AdminLTE3 layout structure

Absolutely! Here's a simple **visual diagram** of the AdminLTE3 layout structure, showing how the header, sidebar, content, and footer relate. I’ll make it text-based but structured so it’s easy to read:

![alt text](image.png)

### Key Points:

* **Header (`main_header`)**: Full-width at the top, always visible; contains nav links, brand/logo, user menu.
* **Sidebar (`main_sidebar`)**: Vertical navigation on the left; can collapse/expand; blocks for logo, user panel, menu links.
* **Content (`content-wrapper`)**: Main area for page-specific content; fills remaining space beside sidebar.
* **Footer (`main_footer`)**: Full-width at the bottom; contains blocks like `footer_text` and `footer_version`.

This diagram mirrors how AdminLTE3 structures the HTML: **header at the top, sidebar on the left, main content in the center/right, footer at the bottom**.



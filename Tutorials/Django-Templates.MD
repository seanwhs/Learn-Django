# 🌐 **Django Templates Tutorial**

Django templates define **how data is displayed to the user**.
They combine **HTML** with **Django Template Language (DTL)**: a powerful syntax for inserting data, looping, conditions, etc.

Templates are usually stored in:

```
app_name/
    templates/
        app_name/
            file.html
```

---

# 📌 **1. Creating Your First Template**

Create a template file:

`app/templates/app/home.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Hello Django!</h1>
</body>
</html>
```

---

# 📌 **2. Rendering a Template in a View**

`app/views.py`

```python
from django.shortcuts import render

def home(request):
    return render(request, 'app/home.html')
```

Add URL:

`mysite/urls.py`

```python
from django.urls import path
from app.views import home

urlpatterns = [
    path('', home),
]
```

Visit:

```
http://127.0.0.1:8000/
```

---

# 📌 **3. Template Variables**

Pass data from the view to the template:

### View:

```python
def home(request):
    context = {'user_name': 'Alice'}
    return render(request, 'app/home.html', context)
```

### Template:

```html
<h1>Welcome, {{ user_name }}!</h1>
```

Variables are surrounded by **double curly braces**: `{{ ... }}`.

---

# 📌 **4. Template Tags**

Tags let you add logic to templates.

### Example: `if`

```html
{% if user_name %}
    <p>Hello, {{ user_name }}!</p>
{% else %}
    <p>Guest User</p>
{% endif %}
```

### Example: `for`

```html
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

---

# 📌 **5. Template Filters**

Filters transform values.

Examples:

```html
{{ name|upper }}
{{ description|truncatewords:10 }}
{{ price|floatformat:2 }}
{{ date|date:"F d, Y" }}
```

Common filters:

| Filter    | Example  | Output         |                 |
| --------- | -------- | -------------- | --------------- |
| `upper`   | `"hello" | upper`         | `"HELLO"`       |
| `lower`   | `"Hi"    | lower`         | `"hi"`          |
| `length`  | `list    | length`        | number of items |
| `default` | `value   | default:"N/A"` | N/A if empty    |

---

# 📌 **6. Template Inheritance (VERY IMPORTANT)**

This avoids repeating HTML on every page.

---

### Step 1: Create a base template

`templates/base.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>

<nav>
    <a href="/">Home</a>
    <a href="/about/">About</a>
</nav>

<hr>

{% block content %}
{% endblock %}

</body>
</html>
```

---

### Step 2: Extend the base template

`templates/app/home.html`

```html
{% extends "base.html" %}

{% block title %}Homepage{% endblock %}

{% block content %}
<h1>Welcome Home</h1>
<p>This is the home page.</p>
{% endblock %}
```

---

# 📌 **7. Including Reusable Template Parts**

You can include other templates:

```html
{% include "partials/footer.html" %}
```

Example:

`templates/partials/footer.html`

```html
<p>© 2025 MySite</p>
```

---

# 📌 **8. Static Files in Templates (CSS, JS, Images)**

Enable static files:

In `settings.py`:

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

Folder:

```
static/
    css/style.css
```

Load and use in templates:

```html
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

---

# 📌 **9. Template Comments**

```html
{# This is a Django template comment #}
```

---

# 📌 **10. Escaping vs. Safe HTML**

Django escapes HTML for security.

```html
{{ text }}  <!-- Safe -->
{{ text|safe }}  <!-- Renders raw HTML (use carefully) -->
```

---

# 📌 **11. Using the `url` Tag**

Instead of hardcoding URLs:

```html
<a href="{% url 'home' %}">Home</a>
```

If your path is:

```python
path("", home, name="home")
```

---

# 📌 **12. Template Organization Best Practices**

✔ Use a **global templates folder** or per-app templates
✔ Always use **extends** to avoid duplication
✔ Store partials in a `partials/` folder
✔ Use `url` tags instead of writing URLs manually
✔ Keep logic out of templates—use views for heavy processing

---

# 🎉 **You Now Understand Django Templates!**

You've learned:

✅ Template structure
✅ Variables, tags, filters
✅ Loops & conditionals
✅ Template inheritance
✅ Static files
✅ Includes and layout reuse
✅ URL resolution
✅ Best practices



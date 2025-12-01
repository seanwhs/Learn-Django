# 🌟 **Reusable Django App Template**

```
myapp_template/
│
├─ myapp/                      # App code
│   ├─ __init__.py
│   ├─ admin.py
│   ├─ apps.py
│   ├─ models.py
│   ├─ views.py
│   ├─ urls.py
│   ├─ forms.py
│   ├─ templatetags/
│   │   ├─ __init__.py
│   │   └─ myapp_tags.py
│   ├─ templates/
│   │   └─ myapp/
│   │       └─ base.html
│   └─ static/
│       └─ myapp/
│           └─ style.css
│
├─ tests/                      # Tests for the app
│   ├─ __init__.py
│   ├─ test_models.py
│   ├─ test_views.py
│   └─ test_forms.py
│
├─ setup.py                    # Packaging info
├─ MANIFEST.in                 # Include templates & static files
├─ README.md
├─ LICENSE
└─ .gitignore
```

---

## **1. setup.py Example**

```python
from setuptools import setup, find_packages

setup(
    name="myapp",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Django>=3.2"],
    author="Your Name",
    author_email="you@example.com",
    description="A reusable Django app template",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/myapp",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
```

---

## **2. MANIFEST.in Example**

```
include README.md LICENSE
recursive-include myapp/templates *
recursive-include myapp/static *
```

---

## **3. Example apps.py**

```python
from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"
```

---

## **4. Example urls.py**

```python
from django.urls import path
from . import views

app_name = "myapp"

urlpatterns = [
    path("", views.home, name="home"),
]
```

---

## **5. Example views.py**

```python
from django.shortcuts import render

def home(request):
    return render(request, "myapp/base.html")
```

---

## **6. Example template**

`templates/myapp/base.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>My App Template</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'myapp/style.css' %}">
</head>
<body>
    <h1>Welcome to My Reusable App!</h1>
</body>
</html>
```

---

## **7. Example static file**

`static/myapp/style.css`

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
    color: #333;
}
```

---

## **8. Example test file**

`tests/test_views.py`

```python
from django.test import TestCase
from django.urls import reverse

class MyAppViewsTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('myapp:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/base.html')
```

---

## **9. Adding Custom Template Tags (Optional)**

`templatetags/myapp_tags.py`

```python
from django import template

register = template.Library()

@register.filter
def shout(value):
    return value.upper() + "!"
```

Usage in templates:

```html
{{ "hello"|shout }}
```

---

## **10. Installation / Local Testing**

1. Build the package:

```bash
python setup.py sdist bdist_wheel
```

2. Install locally:

```bash
pip install dist/myapp-0.1.0-py3-none-any.whl
```

3. Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "myapp",
]
```

4. Include URLs:

```python
path("myapp/", include("myapp.urls")),
```

5. Run server and test:

```bash
python manage.py runserver
```

---

## ✅ **Ready-to-Publish Checklist**

* [x] App folder structure
* [x] setup.py & MANIFEST.in
* [x] Namespaced templates & static files
* [x] Namespaced URLs
* [x] Optional settings handled properly
* [x] Example tests
* [x] README & LICENSE included
* [x] Version set (`__version__ = "0.1.0"`)
* [x] Build and install tested



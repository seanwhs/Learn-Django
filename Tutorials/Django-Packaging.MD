# 🌐 **Packing Django Apps Tutorial**

Packing Django refers to **turning a Django app or project into a reusable, distributable package**—so it can be installed via `pip`, shared with other projects, or published on PyPI.

This is crucial for **reusable apps, libraries, or internal company packages**.

---

# 📌 **1. What You Can Pack**

* **Reusable Apps** – independent Django apps (e.g., polls, comments, notifications)
* **Projects** – usually less common; better to pack as a template/project generator
* **Libraries** – utilities, mixins, template tags, middleware

---

# 📌 **2. Recommended Structure for a Reusable Django App**

```
myapp/
    myapp/
        __init__.py
        admin.py
        apps.py
        models.py
        views.py
        urls.py
        templates/
            myapp/
                *.html
        static/
            myapp/
                *.css / *.js / *.png
        templatetags/
            __init__.py
            myapp_tags.py
    tests/
        __init__.py
        test_models.py
        test_views.py
    setup.py
    README.md
    LICENSE
    MANIFEST.in
```

Key points:

* **Inner `myapp/`** contains the actual app code
* **Outer `myapp/`** is the package root
* **tests/** is optional but recommended
* **setup.py** describes the package
* **MANIFEST.in** ensures templates/static files are included

---

# 📌 **3. Create setup.py**

This file allows the package to be installed with `pip`.

```python
from setuptools import setup, find_packages

setup(
    name="myapp",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,  # include static & templates
    install_requires=[
        "Django>=3.2",
    ],
    author="Your Name",
    author_email="you@example.com",
    description="A reusable Django app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/myapp",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
```

---

# 📌 **4. Include Templates & Static Files (MANIFEST.in)**

```
include README.md LICENSE
recursive-include myapp/templates *
recursive-include myapp/static *
```

This ensures templates and static files are included in distributions.

---

# 📌 **5. Versioning**

* Use semantic versioning: `MAJOR.MINOR.PATCH`
* Example:

```python
# myapp/__init__.py
__version__ = "0.1.0"
```

* Increment minor/major versions as features are added or breaking changes occur.

---

# 📌 **6. Packaging Commands**

Build distribution:

```bash
python setup.py sdist bdist_wheel
```

* `sdist` → source distribution (tar.gz)
* `bdist_wheel` → binary distribution (.whl)

Install locally to test:

```bash
pip install dist/myapp-0.1-py3-none-any.whl
```

---

# 📌 **7. Testing the Package**

1. Create a new Django project
2. Add `myapp` to `INSTALLED_APPS`
3. Include URLs, templates, and static files
4. Run migrations if models exist

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Ensure everything works as expected.

---

# 📌 **8. Publishing on PyPI**

1. Install twine:

```bash
pip install twine
```

2. Upload:

```bash
twine upload dist/*
```

3. Install via pip:

```bash
pip install myapp
```

---

# 📌 **9. Optional: Packaging a Full Django Project Template**

If you want to pack an **entire project template**:

1. Create a template folder:

```
mytemplate/
    project_name/
        manage.py
        project_name/
            settings.py
            urls.py
            wsgi.py
```

2. Use [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django) for automation
3. Pack it with `setup.py` or provide as a zip/tar archive

---

# 📌 **10. Best Practices**

✔ Keep apps independent (no project-specific imports)
✔ Use namespaced templates & static files
✔ Provide optional settings with defaults
✔ Include tests for your app
✔ Add a README with usage instructions
✔ Use semantic versioning
✔ Include a LICENSE file
✔ Include `MANIFEST.in` for non-Python files
✔ Test installation in a fresh virtual environment
✔ Keep dependencies minimal

---

# 🎉 **You Now Know How to Pack Django Apps**

You learned:

✅ App/project structure for packaging
✅ Writing `setup.py` and `MANIFEST.in`
✅ Versioning and metadata
✅ Building source and wheel distributions
✅ Installing locally for testing
✅ Publishing to PyPI
✅ Best practices for reusable Django apps




# 🌟 **Reusable Django App Packaging Checklist**

---

## **1. Project Structure**

✅ App is structured correctly:

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
        static/
            myapp/
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

* Inner `myapp/` contains the code
* Templates and static files are namespaced (`myapp/`)
* Tests are separated

---

## **2. Metadata & `setup.py`**

✅ Include:

* `name`, `version`, `author`, `author_email`
* `description`, `long_description`
* `url` (GitHub or homepage)
* `packages=find_packages()`
* `include_package_data=True`
* `install_requires` for dependencies
* `classifiers` for PyPI

Example:

```python
setup(
    name="myapp",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Django>=3.2"],
    author="Your Name",
    author_email="you@example.com",
    description="A reusable Django app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/myapp",
)
```

---

## **3. Include Non-Python Files**

✅ Create `MANIFEST.in`:

```
include README.md LICENSE
recursive-include myapp/templates *
recursive-include myapp/static *
```

* Ensures templates and static files are included in distributions

---

## **4. Templates & Static Files**

✅ Namespaced:

* Templates: `templates/myapp/*.html`
* Static: `static/myapp/*`

✅ Use `{% load static %}` in templates
✅ Avoid conflicts with other apps

---

## **5. URLs & Views**

✅ Namespaced URLs:

```python
# myapp/urls.py
app_name = "myapp"
urlpatterns = [path("", views.home, name="home")]
```

✅ Use `reverse` in views/templates
✅ Avoid hardcoding paths

---

## **6. Optional Settings**

✅ Avoid project-specific imports
✅ Provide defaults via `django.conf.settings`:

```python
MYAPP_OPTION = getattr(settings, "MYAPP_OPTION", True)
```

✅ Document all optional settings in README

---

## **7. Models & ORM**

✅ Keep models independent
✅ Use `related_name` for relationships
✅ Implement `__str__()` for readability
✅ Include custom methods where needed
✅ Provide `get_absolute_url()` if applicable

---

## **8. Forms**

✅ Reusable forms with proper validation
✅ Avoid project-specific logic
✅ Document usage examples

---

## **9. Template Tags & Filters**

✅ If providing custom tags:

* Create `templatetags/` directory
* Include `__init__.py`
* Register tags with `template.Library()`

Example:

```python
@register.filter
def shout(value):
    return value.upper() + "!"
```

---

## **10. Testing**

✅ Include `tests/` folder with:

* `test_models.py`
* `test_views.py`
* `test_forms.py`

✅ Use `django.test.TestCase`
✅ Cover:

* Models
* Views
* Forms
* URLs
* Template rendering

✅ Run tests locally:

```bash
python manage.py test myapp
```

---

## **11. Documentation**

✅ Include `README.md`:

* Installation instructions
* Usage examples
* Optional settings
* URL and template usage

✅ Include `CHANGELOG.md` for version history
✅ Include LICENSE file

---

## **12. Versioning**

✅ Semantic versioning: `MAJOR.MINOR.PATCH`
✅ Update `__version__` in `__init__.py`:

```python
__version__ = "0.1.0"
```

✅ Tag releases in Git if using version control

---

## **13. Packaging & Distribution**

✅ Build distributions:

```bash
python setup.py sdist bdist_wheel
```

✅ Test installation locally:

```bash
pip install dist/myapp-0.1.0-py3-none-any.whl
```

✅ Optional: Upload to PyPI via Twine:

```bash
pip install twine
twine upload dist/*
```

---

## **14. Optional Enhancements**

✅ Include CLI management commands
✅ Provide admin integration (`admin.py`)
✅ Translation support (`locale/`)
✅ Continuous Integration (GitHub Actions, Travis CI, GitLab CI)
✅ Code formatting (`black`, `flake8`)

---

# ✅ **Quick Checklist Summary Table**

| Task                                    | Done |
| --------------------------------------- | ---- |
| App folder structure correct            | ☐    |
| `setup.py` complete                     | ☐    |
| `MANIFEST.in` includes templates/static | ☐    |
| Templates & static namespaced           | ☐    |
| Namespaced URLs                         | ☐    |
| Optional settings documented            | ☐    |
| Models & forms reusable                 | ☐    |
| Template tags/filters working           | ☐    |
| Tests included & passing                | ☐    |
| README, LICENSE, CHANGELOG              | ☐    |
| Versioning & `__version__`              | ☐    |
| Build & install tested                  | ☐    |
| PyPI upload ready                       | ☐    |

---

This checklist is **all you need to make sure your Django app is reusable, testable, and ready for distribution**.



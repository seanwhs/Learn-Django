# 🌐 **Django Testing Tutorial**

Testing ensures your Django applications are **reliable**, **maintainable**, and **bug-free**. Django comes with a **robust testing framework** built on Python’s `unittest`.

---

# 📌 **1. Why Test Django Apps?**

* Catch bugs before deployment
* Ensure new features don’t break old ones
* Improve maintainability and refactoring confidence
* Document expected behavior

Django encourages **TDD (Test-Driven Development)**.

---

# 📌 **2. Django Test Structure**

Tests live in:

```
myapp/
    tests.py
```

Or for larger apps:

```
myapp/
    tests/
        __init__.py
        test_models.py
        test_views.py
        test_forms.py
        test_urls.py
```

---

# 📌 **3. Basic Test Case**

Django uses `django.test.TestCase`, which inherits from Python’s `unittest.TestCase`.

```python
from django.test import TestCase
from .models import Book

class BookModelTest(TestCase):
    def setUp(self):
        Book.objects.create(title="Django 101", author="Alice")

    def test_book_creation(self):
        book = Book.objects.get(title="Django 101")
        self.assertEqual(book.author, "Alice")
```

* `setUp()` runs before each test
* Use assertions like `assertEqual`, `assertTrue`, `assertFalse`, `assertRaises`

---

# 📌 **4. Testing Models**

Example: validate custom methods and constraints

```python
class BookMethodTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Long Book", pages=400)

    def test_is_long_method(self):
        self.assertTrue(self.book.is_long())
```

Test `__str__()`:

```python
self.assertEqual(str(self.book), "Long Book")
```

---

# 📌 **5. Testing Views**

Use Django’s `Client` to simulate requests.

```python
from django.test import TestCase, Client
from django.urls import reverse
from .models import Book

class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(title="Django 101", author="Alice")

    def test_list_view_status_code(self):
        url = reverse('books:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        url = reverse('books:list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'books/list.html')

    def test_detail_view_context(self):
        url = reverse('books:detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.context['book'], self.book)
```

---

# 📌 **6. Testing Forms**

Validate forms and field errors.

```python
from django.test import TestCase
from .forms import BookForm

class BookFormTest(TestCase):
    def test_valid_form(self):
        data = {'title': 'Django 101', 'author': 'Alice', 'pages': 200}
        form = BookForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'title': '', 'author': 'Alice', 'pages': 200}
        form = BookForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
```

---

# 📌 **7. Testing URLs and Routing**

```python
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import book_list

class UrlTest(SimpleTestCase):
    def test_list_url_resolves(self):
        url = reverse('books:list')
        self.assertEqual(resolve(url).func, book_list)
```

---

# 📌 **8. Testing Admin**

You can test admin pages with the client:

```python
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Book

class AdminTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='pass')
        self.client.login(username='admin', password='pass')
        self.book = Book.objects.create(title="Admin Test", author="Alice")

    def test_admin_list_view(self):
        url = reverse('admin:myapp_book_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_add_view(self):
        url = reverse('admin:myapp_book_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
```

---

# 📌 **9. Testing Model Validation**

```python
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):
    def test_discount_cannot_exceed_price(self):
        from .models import Product
        product = Product(price=50, discount=100)
        with self.assertRaises(ValidationError):
            product.full_clean()
```

---

# 📌 **10. Using Factories and Fixtures**

* **Fixtures**: Preload test data

```python
fixtures = ['books.json']
```

* **Factory Boy**: Generate objects dynamically

```python
import factory
from .models import Book

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = "Factory Book"
    author = "Factory Author"
```

---

# 📌 **11. Running Tests**

```bash
python manage.py test
```

Options:

* `python manage.py test myapp` – specific app
* `--verbosity=2` – more output
* `--failfast` – stop at first failure

---

# 📌 **12. Best Practices for Django Testing**

✔ Test models, views, forms, and URLs
✔ Use `setUpTestData()` for class-level data initialization (faster)
✔ Avoid database dependency for unit tests where possible
✔ Use factories for dynamic data
✔ Isolate tests: they should be independent
✔ Use `Client` to simulate GET/POST requests
✔ Test validation and edge cases
✔ Test permissions and authentication

---

# 🎉 **You Now Understand Django Testing!**

You learned:

✅ Writing unit tests for models
✅ Testing views and templates
✅ Form validation tests
✅ URL and routing tests
✅ Admin tests
✅ Model validation tests
✅ Using fixtures and factories
✅ Running tests and best practices


# 🌐 **Django REST API Tutorial**

Django REST Framework (DRF) is the **de facto standard for building RESTful APIs in Django**. It provides serializers, viewsets, routers, authentication, and more.

---

## **1. Setup**

### Install Django and DRF:

```bash
pip install django djangorestframework
```

### Create a Django project:

```bash
django-admin startproject myapi
cd myapi
```

### Create an app:

```bash
python manage.py startapp notes
```

### Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'notes',
]
```

---

## **2. Create a Model**

`notes/models.py`:

```python
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## **3. Create a Serializer**

Serializers convert Django models to JSON.

`notes/serializers.py`:

```python
from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at']
```

---

## **4. Create API Views**

DRF supports **function-based views**, **class-based views**, and **viewsets**.

### Using `ModelViewSet` (recommended):

`notes/views.py`:

```python
from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
```

---

## **5. Add URLs with Routers**

DRF routers automatically generate CRUD endpoints.

`notes/urls.py`:

```python
from rest_framework import routers
from .views import NoteViewSet

router = routers.DefaultRouter()
router.register(r'notes', NoteViewSet)

urlpatterns = router.urls
```

Include in project `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('notes.urls')),
]
```

Now your API endpoints:

* `GET /api/notes/` → list notes
* `POST /api/notes/` → create note
* `GET /api/notes/{id}/` → retrieve note
* `PUT /api/notes/{id}/` → update note
* `DELETE /api/notes/{id}/` → delete note

---

## **6. Test API with DRF Browsable API**

Run the server:

```bash
python manage.py runserver
```

Visit: **[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)**

You can interact with the API directly from your browser.

---

## **7. Add Authentication (Optional but Recommended)**

DRF supports multiple authentication schemes:

### Token Authentication

1. Install:

```bash
pip install djangorestframework-simplejwt
```

2. Add to `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

3. Add endpoints for token:

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

Now clients can obtain JWT tokens and access protected endpoints.

---

## **8. Filtering, Searching, and Pagination**

### Filtering:

```python
from rest_framework import viewsets, filters

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
```

* Example: `GET /api/notes/?search=django`

### Pagination:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5
}
```

---

## **9. Permissions**

Restrict access using DRF permissions:

```python
from rest_framework.permissions import IsAuthenticated

class NoteViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = [IsAuthenticated]
```

Common permissions:

* `AllowAny` → public access
* `IsAuthenticated` → logged-in users
* `IsAdminUser` → admin only
* Custom permissions by subclassing `BasePermission`

---

## **10. Testing Your API**

DRF provides a test client:

```python
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Note

class NoteAPITest(APITestCase):
    def test_create_note(self):
        url = reverse('note-list')
        data = {'title': 'Test', 'content': 'This is a test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
```

Run tests:

```bash
python manage.py test
```

---

## **11. Best Practices for Django REST APIs**

✔ Use serializers to validate data
✔ Use `ModelViewSet` + routers for CRUD
✔ Protect endpoints with authentication & permissions
✔ Use filtering, searching, and pagination
✔ Version your API (`/api/v1/notes/`)
✔ Document with Swagger / DRF-YASG
✔ Write tests for all endpoints

---

# 🎉 **You Now Have a Full Django REST API**

✅ CRUD endpoints
✅ Browsable API
✅ JWT authentication
✅ Filtering & pagination
✅ Tests
✅ Best practices



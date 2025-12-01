# 🌐 **Django Admin Tutorial**

Django Admin is a powerful, auto-generated backend interface for managing your application’s data.
It is built into Django and can manage any model you register.

---

# 📌 **1. Enabling Django Admin**

Django admin is included by default when you create a project.

Make sure these apps are in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Run migrations to create admin tables:

```bash
python manage.py migrate
```

---

# 📌 **2. Create a Superuser**

This user can access the admin dashboard.

```bash
python manage.py createsuperuser
```

Follow the prompts.

Start the server:

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/admin/
```

Login using your superuser credentials.

---

# 📌 **3. Registering Models in Admin**

To manage a model in the admin, register it.

`app/admin.py`:

```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

Your model now appears in the dashboard.

---

# 📌 **4. Customizing the Admin with `ModelAdmin`**

Create a custom admin class:

```python
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at')
    list_filter = ('author', 'published_at')
    search_fields = ('title', 'author__name')
    ordering = ('published_at',)
```

Register with the model:

```python
admin.site.register(Book, BookAdmin)
```

---

# 📌 **5. Admin List Page Features**

### ✔ `list_display`

Controls which columns appear.

```python
list_display = ('title', 'price', 'stock')
```

### ✔ `list_filter`

Adds filtering sidebar.

```python
list_filter = ('category', 'created_at')
```

### ✔ `search_fields`

Enables full-text search.

```python
search_fields = ('name', 'description')
```

Use `__` to search related models:

```python
search_fields = ('author__name',)
```

### ✔ `ordering`

Sort default admin list view.

```python
ordering = ('-created_at',)
```

---

# 📌 **6. Read-Only Fields**

Make fields uneditable:

```python
readonly_fields = ('created_at', 'updated_at')
```

---

# 📌 **7. Customizing Form Layout (Fieldsets)**

Organize form layout:

```python
fieldsets = (
    ('General Info', {
        'fields': ('title', 'author')
    }),
    ('Publishing', {
        'fields': ('published_at',),
        'classes': ('collapse',)
    }),
)
```

---

# 📌 **8. Inline Models (Editing Related Models on the Same Page)**

Best for relationships like:

* One-to-Many
* Many-to-Many (through tables)

### Example: A Book has many Reviews

`admin.py`:

```python
from .models import Book, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class BookAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
```

Two inline styles:

* `TabularInline` — table layout
* `StackedInline` — card layout

---

# 📌 **9. Custom Admin Actions**

Add actions to the list page.

Example: Approve selected reviews.

```python
def approve_reviews(modeladmin, request, queryset):
    queryset.update(approved=True)

approve_reviews.short_description = "Approve selected reviews"

class ReviewAdmin(admin.ModelAdmin):
    actions = [approve_reviews]
```

---

# 📌 **10. Customizing Admin Display**

### ✔ Change site title and header:

`mysite/admin.py`:

```python
from django.contrib import admin

admin.site.site_header = "MySite Admin"
admin.site.site_title = "MySite Admin Portal"
admin.site.index_title = "Welcome to the Dashboard"
```

---

# 📌 **11. Adding Pagination**

```python
list_per_page = 20
```

---

# 📌 **12. Permissions and Access Control**

Django admin integrates with Django’s auth system.

### Restrict access to certain models:

```python
class BookAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser
```

### Restrict delete:

```python
def has_delete_permission(self, request, obj=None):
    return False
```

### Limit which data users can see:

```python
def get_queryset(self, request):
    qs = super().get_queryset(request)
    return qs.filter(owner=request.user)
```

---

# 📌 **13. Adding Custom Widgets and Form Fields**

Override the default admin form:

```python
from django import forms

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }

class BookAdmin(admin.ModelAdmin):
    form = BookForm
```

---

# 📌 **14. Admin Filters (Advanced)**

Custom filters:

```python
class RatingFilter(admin.SimpleListFilter):
    title = 'Rating'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [('high', 'High (4-5)'), ('low', 'Low (1-3)')]

    def queryset(self, request, qs):
        if self.value() == 'high':
            return qs.filter(rating__gte=4)
        if self.value() == 'low':
            return qs.filter(rating__lte=3)
```

Add to admin:

```python
list_filter = (RatingFilter,)
```

---

# 📌 **15. Custom Admin Pages (Admin Views)**

You can add custom views:

```python
from django.urls import path
from django.template.response import TemplateResponse

class BookAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('report/', self.admin_site.admin_view(self.report_view))
        ]
        return custom_urls + urls

    def report_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            books=Book.objects.all()
        )
        return TemplateResponse(request, "admin/book_report.html", context)
```

---

# 📌 **16. Admin Themes (Styling the Admin)**

You can use external themes:

* Django Jazzmin
* Django Grappelli
* Django Jet

Example for **Jazzmin**:

```bash
pip install django-jazzmin
```

Add in settings:

```python
INSTALLED_APPS = [
    "jazzmin",
    ...
]
```

Instant UI upgrade.

---

# 📌 **17. Best Practices for Django Admin**

✔ Use `ModelAdmin` for every model
✔ Add search + filters for large tables
✔ Use read-only fields for timestamps
✔ Restrict permissions for non-admin staff
✔ Use inline models for related data
✔ Add custom actions for batch operations
✔ Override forms for better UX
✔ Avoid heavy queries in admin (use list_select_related)

---

# 🎉 **You Now Understand Django Admin!**

You learned:

✅ Admin setup
✅ Registering models
✅ Customizing list pages
✅ Search + filters
✅ Inlines
✅ Custom admin actions
✅ Permissions
✅ Custom pages
✅ Admin theming
✅ Best practices


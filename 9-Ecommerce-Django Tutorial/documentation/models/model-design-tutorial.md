# **Django Model Design Tutorial**

Django models define your application’s **data structure and behavior**. Well-designed models improve **maintainability, scalability, and performance**.

---

## **1. Introduction to Django Models**

A Django model is a Python class that inherits from `django.db.models.Model`. Each attribute maps to a database column.

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.IntegerField()

    def __str__(self):
        return self.title
```

**Key Points:**

* Field types like `CharField`, `IntegerField`, and `DateField` define column types.
* `unique=True` enforces uniqueness.
* `__str__` provides a human-readable string representation.

---

## **2. Choosing Field Types**

| Field Type                   | Use Case                               |
| ---------------------------- | -------------------------------------- |
| `CharField`                  | Short text (names, titles)             |
| `TextField`                  | Long text (descriptions, articles)     |
| `IntegerField`               | Whole numbers                          |
| `FloatField`                 | Floating-point numbers                 |
| `DecimalField`               | Precise decimals (money, calculations) |
| `BooleanField`               | True/False values                      |
| `DateField`, `DateTimeField` | Dates and timestamps                   |
| `ForeignKey`                 | One-to-many relationships              |
| `ManyToManyField`            | Many-to-many relationships             |
| `OneToOneField`              | One-to-one relationships               |

> **Tip:** Use the most specific field type possible for validation, indexing, and performance.

---

## **3. Defining Relationships**

### **3.1 One-to-Many (`ForeignKey`)**

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
```

* `on_delete=models.CASCADE`: Deletes related books when the author is removed.
* Alternatives: `SET_NULL`, `PROTECT`, `DO_NOTHING`.

### **3.2 Many-to-Many (`ManyToManyField`)**

```python
class Course(models.Model):
    name = models.CharField(max_length=100)

class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)
```

### **3.3 One-to-One (`OneToOneField`)**

```python
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
```

---

## **4. Model Meta Options**

Meta options customize model behavior:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    published_date = models.DateField()

    class Meta:
        ordering = ['published_date']  # Default sort order
        verbose_name = "Book"
        verbose_name_plural = "Books"
```

* `ordering`: Default sort order for queries.
* `verbose_name` / `verbose_name_plural`: Human-readable names.
* `unique_together`: Composite uniqueness constraints.

---

## **5. Methods and Properties**

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    pages = models.IntegerField()

    def is_long_book(self):
        return self.pages > 500
```

* Use `@property` for computed fields.
* Keep business logic in models for a **“fat models, thin views”** design.

---

## **6. Best Practices**

1. **Normalize data** to avoid redundancy.
2. **Use appropriate field types** for validation and performance.
3. **Implement `__str__`** for readability.
4. **Keep models modular**, separating unrelated concerns.
5. **Use `choices` for enums**:

```python
class Book(models.Model):
    GENRE_CHOICES = [
        ('FIC', 'Fiction'),
        ('NF', 'Non-Fiction'),
        ('SCI', 'Science'),
    ]
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=3, choices=GENRE_CHOICES)
```

6. **Index frequently queried fields**:

```python
title = models.CharField(max_length=200, db_index=True)
```

7. **Use `related_name` for reverse lookups**:

```python
author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
```

---

## **7. Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

* `makemigrations`: Generates migration files.
* `migrate`: Applies changes to the database.

---

## **8. Advanced Concepts**

* **Abstract Models**: Base class for shared fields.

```python
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

* **Proxy Models**: Modify Python behavior without changing the database.
* **Custom Managers**:

```python
class BookManager(models.Manager):
    def long_books(self):
        return self.filter(pages__gt=500)

class Book(models.Model):
    title = models.CharField(max_length=200)
    pages = models.IntegerField()

    objects = BookManager()
```

---

## ✅ **Summary**

* Models define database structure and behavior.
* Use proper fields, relationships, and `Meta` options.
* Add methods, properties, and managers for maintainability.
* Apply migrations to safely update the database.

---

# **Django Generic Models (GenericForeignKey)**

Generic models allow a single model to relate to **any other model** using Django’s `contenttypes` framework.

---

## **1. When to Use Generic Models**

* One model must relate to multiple models.
* Avoid multiple ForeignKeys.
* Useful for **comments, tags, likes, or activity logs**.

**Example:** A `Comment` that can attach to `BlogPost`, `Photo`, or `Video`.

---

## **2. Implementing Generic Models**

```python
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.content_object}"
```

* `content_type`: Model being referenced.
* `object_id`: Primary key of the instance.
* `content_object`: Resolves dynamically to the actual Python object.

---

## **3. Using Generic Models**

```python
post = BlogPost.objects.create(title="Django Tips", body="...")
photo = Photo.objects.create(caption="Sunset")

Comment.objects.create(content_object=post, text="Great post!")
Comment.objects.create(content_object=photo, text="Beautiful photo!")
```

* `content_object` automatically handles the target model and ID.

---

## **4. Reverse Generic Relations**

```python
from django.contrib.contenttypes.fields import GenericRelation

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    comments = GenericRelation(Comment)
```

```python
post.comments.all()
```

* Query related comments directly without filtering by `ContentType`.

---

## **5. Best Practices**

1. Use GenericForeignKey only when necessary.
2. Index `object_id` for performance.
3. Use `GenericRelation` for reverse lookups.
4. Generic relations **don’t enforce database-level foreign key constraints**.
5. Plan migrations carefully for related models.

---

## **6. Example: Tagging System**

```python
class Tag(models.Model):
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
```

* Allows tagging **any model** with a single `Tag` model.

---

## ✅ **Summary**

* Generic models allow flexible relationships to multiple models.
* Use Django’s `contenttypes` framework: `ContentType`, `GenericForeignKey`, `GenericRelation`.
* Ideal for comments, tags, and activity logs.
* Trade-offs: less strict integrity and slightly slower queries.

---

# **Django Model Relationships (ASCII UML)**

```
STANDARD RELATIONSHIPS
----------------------

+---------+           +---------+
| Author  |1--------* |  Book   |
+---------+           +---------+
| name    |           | title   |
+---------+           +---------+

+---------+           +---------+
| Course  |*--------* | Student |
+---------+           +---------+
| name    |           | name    |
+---------+           +---------+

+---------+           +---------+
|  User   |1--------1 | Profile |
+---------+           +---------+
| username|           | bio     |
+---------+           +---------+

GENERIC RELATIONSHIPS
---------------------

+-----------+     +---------+     +-------+
| BlogPost  |     |  Photo  |     | Video |
+-----------+     +---------+     +-------+
      \               |             /
       \              |            /
        \             |           /
         +----------------------+
         |      Comment         |
         +----------------------+
         | text                 |
         | content_object       |
         +----------------------+

         +----------------------+
         |        Tag           |
         +----------------------+
         | name                 |
         | content_object       |
         +----------------------+
```

**Legend:**

* `1--------*`: One-to-Many (`ForeignKey`)
* `*--------*`: Many-to-Many (`ManyToManyField`)
* `1--------1`: One-to-One (`OneToOneField`)
* `GenericForeignKey`: Flexible link to multiple models


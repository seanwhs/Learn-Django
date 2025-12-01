# 🌐 **Django Data Validation Tutorial**

Django provides **built-in, secure, and scalable data validation** across models, forms, serializers (DRF), and custom logic.
Validation ensures data is **correct**, **safe**, and **consistent** before saving to a database or processing user input.

This tutorial focuses on **Models + Forms**, the core of Django validation.

---

# 📌 **1. Types of Validation in Django**

### Django validates data in three main places:

1️⃣ **Field-level validation**
Built-in validation for field type, max_length, required, etc.

2️⃣ **Form validation**
Validates user-submitted data in forms and ModelForms.

3️⃣ **Model validation**
Validates data before saving to the database.

4️⃣ **Custom validators**
Reusable functions that validate values.

---

# 📌 **2. Built-in Validation (Automatic)**

Django automatically validates:

* Required fields
* Field lengths
* Data types (Email, Integer, Date, URL)
* Choices
* Unique fields
* Foreign key restrictions

Example:

```python
email = forms.EmailField()
```

This validates:

* Must be an email
* Cannot be blank (unless `required=False`)

---

# 📌 **3. Form Field-Level Validation (`clean_<field>()`)**

Inside a form, you create a method named:

```
clean_fieldname()
```

Example:

```python
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    age = forms.IntegerField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if " " in username:
            raise forms.ValidationError("Username cannot contain spaces.")
        return username

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise forms.ValidationError("You must be at least 18.")
        return age
```

✔ Runs only for that field
✔ Runs **before** the general `clean()` method

---

# 📌 **4. Form-Wide Validation (`clean()`)**

Use this when multiple fields depend on each other.

Example:

```python
class BookingForm(forms.Form):
    start = forms.DateField()
    end = forms.DateField()

    def clean(self):
        data = super().clean()
        start = data.get('start')
        end = data.get('end')

        if start and end and end < start:
            raise forms.ValidationError("End date must be after start date.")
        
        return data
```

✔ Useful for cross-field validation
✔ Runs after all `clean_<field>()` methods

---

# 📌 **5. Model Validation (`clean()` + `full_clean()`)**

Models have their own validation layer too.

```python
from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        if self.discount > self.price:
            raise ValidationError("Discount cannot exceed price.")
```

### When is model validation run?

* In ModelForms (automatically)
* When calling `full_clean()` manually

```python
product = Product(price=10, discount=20)
product.full_clean()   # raises ValidationError
```

⚠ **Note**:
`model.save()` **does NOT** run validation automatically.

---

# 📌 **6. Model Field Validators**

You can attach validators directly to model fields.

```python
from django.core.validators import MinValueValidator, MaxValueValidator

class Rating(models.Model):
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
```

Custom validator:

```python
def validate_no_x(value):
    if "x" in value.lower():
        raise ValidationError("Value cannot contain the letter X.")

class User(models.Model):
    username = models.CharField(max_length=20, validators=[validate_no_x])
```

Reusable and clean!

---

# 📌 **7. Custom ValidationException Messages**

Custom messages for fields:

```python
name = forms.CharField(
    error_messages={
        "required": "Please enter your name.",
        "max_length": "Name is too long!"
    }
)
```

Custom model error messages:

```python
title = models.CharField(
    max_length=50,
    error_messages={
        'unique': 'This title is already taken.'
    }
)
```

---

# 📌 **8. Using `is_valid()` and `cleaned_data`**

```python
form = RegisterForm(request.POST)

if form.is_valid():
    data = form.cleaned_data
    print(data['username'])
else:
    print(form.errors)
```

✔ `is_valid()` runs all form/model validation
✔ `cleaned_data` contains the validated data

---

# 📌 **9. Displaying Validation Errors in Templates**

```html
<form method="post">
    {% csrf_token %}
    {{ form.non_field_errors }}

    {{ form.username.errors }}
    {{ form.username }}

    <button>Submit</button>
</form>
```

Django attaches error messages to the form, field, and template context.

---

# 📌 **10. Validation with ModelForm**

ModelForm automatically runs:

* field validation
* model validators
* model `clean()`

Example:

```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['price', 'discount']
```

In a view:

```python
form = ProductForm(request.POST)
if form.is_valid():
    form.save()
```

---

# 📌 **11. Best Practices for Django Validation**

✔ Use **model-level validation** for business rules
✔ Use **form-level validation** for user input rules
✔ Use `clean_<field>()` for single-field validation
✔ Use `clean()` for cross-field checks
✔ Use reusable **validators** for simple checks
✔ Avoid duplicating validation logic in multiple layers
✔ Use descriptive error messages

---

# 🎉 **You Now Understand Django Data Validation!**

You learned:

✅ Built-in field validation
✅ Form validation (`clean`, `clean_<field>`)
✅ Model validation (`clean`, `full_clean`)
✅ Custom validators
✅ Validation error messaging
✅ Template error display
✅ Best practices



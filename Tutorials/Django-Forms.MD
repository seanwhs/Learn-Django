# 🌐 **Django Forms Tutorial**

Django Forms allow you to:

* Collect user input (HTML forms)
* Validate and clean data securely
* Save data to models
* Render form fields automatically
* Avoid writing repetitive HTML

Django Forms come in two main types:

1. **Forms** — Hand-crafted forms (full control)
2. **ModelForms** — Auto-generated forms tied to models

Let's explore both.

---

# 📌 **1. Creating a Basic Django Form**

Create a new file:

`app/forms.py`

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

### Key points:

* Each field becomes an HTML input.
* Django handles validation automatically (email format, required fields, etc.)
* Widgets define how fields are displayed (`TextInput`, `Textarea`, etc.)

---

# 📌 **2. Using the Form in a View**

`app/views.py`

```python
from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # use data
            return render(request, 'app/success.html')

    return render(request, 'app/contact.html', {'form': form})
```

### Workflow:

1. On GET → render empty form
2. On POST → validate form
3. If valid → access cleaned data
4. Render success page

---

# 📌 **3. Rendering the Form in a Template**

`templates/app/contact.html`

```html
<h1>Contact Us</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Send</button>
</form>
```

### Rendering options:

* `{{ form.as_p }}` → wrapped in `<p>` tags
* `{{ form.as_table }}` → table layout
* `{{ form.as_ul }}` → list items
* Or fully custom HTML

---

# 📌 **4. Form Validation**

### Built-in validation:

* Required fields
* Email format
* Length limits
* Numeric types

### Custom validation example:

```python
class ContactForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith(".com"):
            raise forms.ValidationError("Email must end with .com")
        return email
```

### Validate multiple fields together:

```python
def clean(self):
    cleaned = super().clean()
    email = cleaned.get('email')
    message = cleaned.get('message')

    if email and "spam" in message.lower():
        raise forms.ValidationError("Spam detected!")
```

---

# 📌 **5. Django ModelForm (Most Common & Powerful)**

`ModelForms` automatically create forms based on your models.

### Example model:

```python
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
```

### Create the ModelForm:

`app/forms.py`

```python
from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
```

---

# 📌 **6. Using ModelForm in a View**

`app/views.py`

```python
def create_note(request):
    form = NoteForm()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()  # saves to database
            return redirect('notes_list')

    return render(request, 'app/note_form.html', {'form': form})
```

Easy CRUD operations become very simple!

---

# 📌 **7. Customizing ModelForm Widgets**

Inside `Meta`:

```python
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
```

---

# 📌 **8. Displaying Form Errors**

Inside template:

```html
{% if form.errors %}
<ul>
    {% for field in form %}
        {% for error in field.errors %}
            <li>{{ field.label }}: {{ error }}</li>
        {% endfor %}
    {% endfor %}
</ul>
{% endif %}
```

Django handles:

* Missing fields
* Invalid values
* Custom validation errors

---

# 📌 **9. Handling File Uploads**

### In your form:

```python
class UploadForm(forms.Form):
    file = forms.FileField()
```

### In your view:

```python
form = UploadForm(request.POST, request.FILES)
```

### In template:

```html
<form method="post" enctype="multipart/form-data">
```

---

# 📌 **10. Custom Form Layouts (Manual Rendering)**

Instead of `{{ form.as_p }}`, you can write:

```html
<label>Title:</label>
{{ form.title }}

<label>Message:</label>
{{ form.message }}
```

Or include errors:

```html
{{ form.title.errors }}
{{ form.title }}
```

This gives full layout control.

---

# 🎉 **You're Now Ready to Use Django Forms!**

You have learned:

✅ Basic Django forms
✅ Handling POST requests
✅ Rendering forms in templates
✅ Built-in and custom validation
✅ ModelForms
✅ Widgets and styling
✅ File uploads
✅ Manual rendering

This is everything you need to build real-world forms in Django.



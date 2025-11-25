# **Mini Django Project: “My Blog”**

We’ll create a simple blog with a home page listing posts and an about page.

---

## **1. Set Up the Project**

```bash
django-admin startproject myblog
cd myblog
python manage.py startapp blog
```

---

## **2. Configure Settings**

In `myblog/settings.py`:

```python
INSTALLED_APPS = [
    # default apps...
    'blog',  # add our app
]

# Templates configuration (default is fine, make sure APP_DIRS=True)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # optional global templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files
STATIC_URL = '/static/'
```

---

## **3. Create URL Routing**

### `myblog/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # direct root to blog app
]
```

### `blog/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]
```

---

## **4. Create Views**

### `blog/views.py`:

```python
from django.shortcuts import render

def home(request):
    posts = [
        {'title': 'First Post', 'author': 'Alice'},
        {'title': 'Second Post', 'author': 'Bob'},
        {'title': 'Third Post', 'author': 'Charlie'},
    ]
    return render(request, 'blog/home.html', {'posts': posts})

def about(request):
    return render(request, 'blog/about.html', {'title': 'About My Blog'})
```

---

## **5. Create Templates**

### **Folder Structure**

```
blog/
    templates/
        blog/
            base.html
            home.html
            about.html
            navbar.html
```

---

### **5.1 `base.html`** (Base template)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Blog{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'blog/style.css' %}">
</head>
<body>
    {% include "blog/navbar.html" %}

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <footer>
        <p>© 2025 My Blog</p>
    </footer>
</body>
</html>
```

---

### **5.2 `navbar.html`** (Navigation snippet)

```html
<nav>
    <a href="{% url 'home' %}">Home</a> |
    <a href="{% url 'about' %}">About</a>
</nav>
<hr>
```

---

### **5.3 `home.html`** (Home page with loop)

```html
{% extends "blog/base.html" %}

{% block title %}Home - My Blog{% endblock %}

{% block content %}
<h1>Blog Posts</h1>
<ul>
    {% for post in posts %}
        <li><strong>{{ post.title }}</strong> by {{ post.author }}</li>
    {% empty %}
        <li>No posts available.</li>
    {% endfor %}
</ul>
{% endblock %}
```

---

### **5.4 `about.html`** (About page)

```html
{% extends "blog/base.html" %}

{% block title %}About - My Blog{% endblock %}

{% block content %}
<h1>{{ title }}</h1>
<p>This is a simple blog built with Django templates!</p>
{% endblock %}
```

---

## **6. Add Static Files**

Create a folder:

```
blog/
    static/
        blog/
            style.css
```

### **`style.css`**:

```css
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    background-color: #f9f9f9;
}

nav a {
    margin-right: 10px;
    text-decoration: none;
    color: #333;
}

.container {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
}

footer {
    margin-top: 20px;
    text-align: center;
    color: gray;
}
```

---

## **7. Run the Project**

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` → Home page with blog posts.
Open `http://127.0.0.1:8000/about/` → About page.

---

✅ **What this project demonstrates:**

1. **Template inheritance** (`base.html`)
2. **Template includes** (`navbar.html`)
3. **Loops in templates** (`home.html` posts)
4. **Context passing from views**
5. **Static files** (`style.css`)

---

If you want, I can make a **next-level version** where clicking a post goes to a **dynamic detail page** using URL parameters and template rendering. This would turn it into a mini real blog.


# **own detail page**
Let’s upgrade our mini blog so that each post has its **own detail page** using URL parameters and template rendering. This will make the blog more dynamic.

---

# **Step 1: Update Views for Post Details**

We’ll pass a `post_id` in the URL and render the details page.

### `blog/views.py`

```python
from django.shortcuts import render, get_object_or_404

# Sample posts data (usually from a database)
posts = [
    {'id': 1, 'title': 'First Post', 'author': 'Alice', 'content': 'This is the first post.'},
    {'id': 2, 'title': 'Second Post', 'author': 'Bob', 'content': 'This is the second post.'},
    {'id': 3, 'title': 'Third Post', 'author': 'Charlie', 'content': 'This is the third post.'},
]

def home(request):
    return render(request, 'blog/home.html', {'posts': posts})

def about(request):
    return render(request, 'blog/about.html', {'title': 'About My Blog'})

def post_detail(request, post_id):
    # Find the post by id
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return render(request, 'blog/404.html', status=404)
    return render(request, 'blog/post_detail.html', {'post': post})
```

---

# **Step 2: Add URL Pattern for Post Details**

### `blog/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
```

Here `<int:post_id>` captures the post ID from the URL.

---

# **Step 3: Update Home Template**

We want each post title to link to its detail page.

### `home.html`

```html
{% extends "blog/base.html" %}

{% block title %}Home - My Blog{% endblock %}

{% block content %}
<h1>Blog Posts</h1>
<ul>
    {% for post in posts %}
        <li>
            <a href="{% url 'post_detail' post.id %}"><strong>{{ post.title }}</strong></a>
            by {{ post.author }}
        </li>
    {% empty %}
        <li>No posts available.</li>
    {% endfor %}
</ul>
{% endblock %}
```

---

# **Step 4: Create Post Detail Template**

### `post_detail.html`

```html
{% extends "blog/base.html" %}

{% block title %}{{ post.title }} - My Blog{% endblock %}

{% block content %}
<h1>{{ post.title }}</h1>
<p><em>by {{ post.author }}</em></p>
<p>{{ post.content }}</p>
<a href="{% url 'home' %}">← Back to Home</a>
{% endblock %}
```

---

# **Step 5: Optional 404 Page**

### `404.html`

```html
{% extends "blog/base.html" %}

{% block title %}Page Not Found{% endblock %}

{% block content %}
<h1>404 - Post Not Found</h1>
<p>Sorry, the post you are looking for does not exist.</p>
<a href="{% url 'home' %}">← Back to Home</a>
{% endblock %}
```

---

# **Step 6: Test the Project**

1. Run the server:

```bash
python manage.py runserver
```

2. Navigate to `http://127.0.0.1:8000/` → Home page
3. Click a post → Goes to `http://127.0.0.1:8000/post/1/` (or 2, 3)
4. Non-existing post ID → Shows 404 page

---

✅ **What we added:**

* **Dynamic URL parameters** for posts
* **`post_detail` view** to render a single post
* **Clickable links** in the home template
* **404 handling** for missing posts


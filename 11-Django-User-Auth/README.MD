# Django Email-Verified Authentication Tutorial

This project demonstrates a **simple Django authentication system** with email verification for account activation. Users must verify their email before they can log in.

---

## **Features**

* User registration (signup)
* Email verification for account activation
* Login and logout
* Custom user model with email as unique field
* Plain HTML templates (no CSS frameworks)

---

## **Project Structure**

```
AUTH/
├─ AUTH/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
├─ authentication/
│  ├─ models.py
│  ├─ forms.py
│  ├─ views.py
│  ├─ urls.py
│  ├─ tokens.py
├─ templates/
│  └─ authentication/
│     ├─ base.html
│     ├─ home.html
│     ├─ signup.html
│     └─ signin.html
├─ db.sqlite3
└─ manage.py
```

---

## **Installation & Setup**

1. Clone the repository:

```bash
git clone <repo-url>
cd AUTH
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

3. Install Django:

```bash
pip install django
```

4. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

---

## **Testing Email Activation**

### **1. Development Mode (Console Backend)**

* Default `settings.py` configuration:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
```

* Steps:

  1. Go to [http://127.0.0.1:8000/signup/](http://127.0.0.1:8000/signup/)
  2. Fill in the signup form and submit
  3. Check the **console output**. You will see an activation link:

```
Hi <FirstName>,

Activate your account:
http://127.0.0.1:8000/activate/<uidb64>/<token>/
```

4. Copy and paste the link in the browser
5. After activation, go to [http://127.0.0.1:8000/signin/](http://127.0.0.1:8000/signin/) to log in

* **Note:** The account remains inactive until the activation link is visited.

---

### **2. Production Mode (SMTP Backend)**

* Update `settings.py` to use your SMTP server:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'   # e.g., smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = 'your-email@example.com'
```

* Steps:

  1. Restart the Django server
  2. Signup at [http://127.0.0.1:8000/signup/](http://127.0.0.1:8000/signup/)
  3. Open your email inbox and locate the activation email
  4. Click the activation link
  5. After activation, log in at [http://127.0.0.1:8000/signin/](http://127.0.0.1:8000/signin/)

* **Notes:**

  * If using Gmail, you may need to create an **App Password** or enable **less secure app access**.
  * The account will not be able to log in until it is activated via email.

---

## **User Flow Summary**

1. User signs up → account created but inactive
2. Activation email sent → user clicks link → account becomes active
3. User can now log in successfully
4. User can log out at any time

---

## **Custom User Model**

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
```

* Set in `settings.py`:

```python
AUTH_USER_MODEL = 'authentication.CustomUser'
```

---

## **Templates**

* `base.html` – Navigation and layout
* `home.html` – Home page
* `signup.html` – Registration form
* `signin.html` – Login form

Plain HTML, no CSS.

---

## **License**

For learning purposes only. Free to use and modify.


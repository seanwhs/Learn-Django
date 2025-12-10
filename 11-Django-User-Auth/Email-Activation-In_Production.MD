# **Production-Ready Django Email Activation (FBV) – Refactored Guide**

This version focuses on **clean separation of concerns, security, maintainability, and production-readiness**, while keeping **function-based views (FBVs)**.

---

## **1. Decouple Email Logic – Utilities**

Instead of embedding email sending in views, we move it into a dedicated utility module. This keeps views clean, allows easy testing, and makes future changes to email logic simpler.

**`authentication/utils.py`**

```python
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token

def send_activation_email(user, request):
    """
    Sends an account activation email to the newly registered user.

    Args:
        user: User instance that needs activation.
        request: HttpRequest object to get domain dynamically.

    Raises:
        Exception: If email sending fails, the exception is propagated.
    """
    # Encode user ID in base64
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Generate a secure token for this user
    token = account_activation_token.make_token(user)
    
    # Build activation link dynamically using the request domain
    domain = request.get_host()
    activation_link = f"http://{domain}/activate/{uidb64}/{token}/"

    # Render the email template with context variables
    subject = "Activate Your Account"
    message = render_to_string('authentication/activation_email.html', {
        'user': user,
        'activation_link': activation_link
    })

    # Send email using Django's send_mail utility
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,  # Raise exception if sending fails
    )
```

**Why this approach is better:**

* Keeps **views lightweight**.
* Allows **HTML email templates** for a professional look.
* Easy to swap SMTP backend or integrate transactional email services like SendGrid.

---

## **2. Email Template for Production**

**`templates/authentication/activation_email.html`**

```html
<!DOCTYPE html>
<html>
<body>
  <p>Hello {{ user.first_name }},</p>
  <p>Welcome! Thanks for registering. Please activate your account by clicking the link below:</p>
  <p><a href="{{ activation_link }}">{{ activation_link }}</a></p>
  <p>If you did not create an account, ignore this email.</p>
  <hr>
  <p>Best regards,<br>Your Website Team</p>
</body>
</html>
```

**Notes:**

* HTML email ensures readability across devices.
* Can add plain-text fallback for clients that don’t render HTML.

---

## **3. Refactored Signup View (Function-Based)**

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm
from .utils import send_activation_email

def signup(request):
    """
    Handles user registration and sends an activation email.

    Flow:
    1. User submits signup form (POST request)
    2. Validate input using SignupForm
    3. Create user with is_active=False
    4. Send activation email
    5. Provide feedback to user and redirect to signin page
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create user but do not activate yet
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Attempt to send activation email
            try:
                send_activation_email(user, request)
            except Exception as e:
                # Log the error in production (not shown here)
                messages.error(request, "Failed to send activation email. Contact support.")
            else:
                messages.success(request, "Account created! Please check your email to activate your account.")

            return redirect('signin')
        else:
            # Form invalid → render errors
            messages.error(request, "Please correct the errors below.")
    else:
        # GET request → empty form
        form = SignupForm()

    return render(request, 'authentication/signup.html', {'form': form})
```

**Production considerations:**

* Prevents login before email activation (`is_active=False`).
* Gracefully handles email sending failure.
* Form errors are displayed to user without losing submitted data.

---

## **4. Activation View (Function-Based)**

```python
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from .tokens import account_activation_token

User = get_user_model()

def activate(request, uidb64, token):
    """
    Handles account activation when user clicks the activation link.

    Steps:
    1. Decode uidb64 to get user ID
    2. Retrieve user from DB
    3. Verify the token
    4. Activate account if valid
    5. Handle invalid or expired tokens gracefully
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated! You can now log in.")
        return redirect('signin')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('signup')
```

**Security & UX considerations:**

* Protects against tampering by validating token.
* Handles invalid links without exposing internal errors.
* User is redirected to signup if activation fails.

---

## **5. Signin View (Function-Based)**

```python
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SigninForm

def signin(request):
    """
    Handles user login.

    Checks:
    1. Valid credentials
    2. User is active (email verified)
    """
    if request.method == 'POST':
        form = SigninForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, "Email not verified. Please activate your account.")
                return redirect('signin')

            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = SigninForm()

    return render(request, 'authentication/signin.html', {'form': form})
```

---

## **6. Signout View (Function-Based)**

```python
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def signout(request):
    """
    Logs out the user and redirects to home.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')
```

---

## **7. Production Email Settings**

**In `settings.py` – Environment-Based Configuration:**

```python
import os

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
```

**Advantages:**

* No sensitive credentials in version control.
* Easy to switch SMTP providers without changing code.
* Can be used with `.env` files locally.

---

## **8. Additional Production Best Practices**

1. **Use Transactional Email Services** – SendGrid, Amazon SES, Mailgun.
2. **Graceful Failure Handling** – Log failed emails without breaking signup.
3. **Token Expiry** – Optional, but adds extra security.
4. **Logging** – Always log errors for monitoring production issues.
5. **HTML + Plain Text Emails** – For compatibility with all email clients.

---

## ✅ **Summary – Why This is Production-Ready**

* **FBVs retained** – simple, readable, no unnecessary complexity.
* **Email logic separated** – `utils.py` for maintainability.
* **Secure token-based activation** – prevents tampering.
* **Graceful error handling** – users informed without breaking workflow.
* **Environment-driven settings** – production safe.
* **HTML email templates** – professional UX.


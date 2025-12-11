# 🔒 Django Authentication Engineering Guide: Full-Stack & Production-Ready

> **Audience:** Developers familiar with Django/DRF basics who need to build a **secure, scalable, and extensible authentication system**.
> **Goal:** A complete deep dive covering Session Auth → JWT (SimpleJWT) → OAuth/OIDC → TOTP, including **code examples, security considerations, and operational guidelines**.

---

## 🧭 0. Architecture & Prerequisites

We aim to build a **decoupled authentication system**:

* **JWT** for API clients (SPA/Mobile)
* **Session Auth** for Django Admin and server-rendered views

### Core Principles

* **Thin Views, Service Layer Logic:** Authentication logic—token management, email, 2FA—is kept in **services/utilities**. Views orchestrate flow only.
* **Secrets Management:** Never hardcode keys; use `.env` for development and a dedicated secrets manager in production.
* **Fail Closed:** Deny access by default; grant permissions explicitly.
* **JWT Security:**

  * Short-lived access tokens (15–30 min)
  * Rotated refresh tokens stored in **HTTP-only cookies**
* **Email Verification:** Enforce verified email addresses (`is_email_verified=True`) for all sign-ups.
* **2FA Optional but Recommended:** Even for internal apps, TOTP reduces the impact of compromised passwords.

### Project Setup

```bash
django-admin startproject authproj
cd authproj
python -m venv venv && source venv/bin/activate
pip install django djangorestframework djangorestframework-simplejwt python-dotenv pyotp qrcode social-auth-app-django psycopg2-binary
python manage.py startapp accounts
python manage.py startapp tenants  # Optional multi-tenancy
```

### Suggested Project Structure

```
authproj/
├── authproj/
│   ├── settings.py
│   └── urls.py
├── accounts/
│   ├── models.py          # CustomUser, TwoFactor
│   ├── serializers.py     # Register, Login, Token, 2FA
│   ├── views.py           # API endpoints
│   ├── backends.py        # Optional LDAP or external auth
│   ├── tokens.py          # JWT & activation utilities
│   └── pipeline.py        # Social auth customization
├── tenants/               # Multi-tenant models
└── .env                   # Environment variables
```

---

## 👥 1. Custom User Model

Always create a **custom user model before running the first migration**. It provides flexibility for email login, multi-tenancy, 2FA flags, and profile attributes.

### `accounts/models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import pyotp

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    tenant = models.ForeignKey(
        "tenants.Tenant",
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def generate_2fa_secret(self):
        """Generate and store TOTP secret for the user."""
        from .models import TwoFactor
        secret = pyotp.random_base32()
        TwoFactor.objects.update_or_create(user=self, defaults={"secret": secret})
        return secret

class TwoFactor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="two_factor"
    )
    secret = models.CharField(max_length=32, blank=True, null=True)
    enabled = models.BooleanField(default=False)
    backup_codes = models.JSONField(default=list)

    def generate_backup_codes(self, n=5):
        """Generate one-time backup codes for 2FA."""
        import secrets
        codes = [secrets.token_hex(4) for _ in range(n)]
        self.backup_codes = codes
        self.save()
        return codes
```

### `tenants/models.py` (Optional Multi-Tenant)

```python
from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
```

### `settings.py` Addition

```python
AUTH_USER_MODEL = "accounts.CustomUser"
# Must be set before the first migration!
```

---

## ⚙️ 2. Core Settings & JWT Configuration

Security-first settings combined with DRF and SimpleJWT.

```python
import os
from datetime import timedelta

DEBUG = os.environ.get("DEBUG", "True") == "True"
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

# Security Settings
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = "Lax"
X_FRAME_OPTIONS = "DENY"

# DRF Authentication
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# JWT Config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": os.environ.get("JWT_SIGNING_KEY", SECRET_KEY),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ALGORITHM": "HS256",
}

INSTALLED_APPS += [
    "rest_framework_simplejwt.token_blacklist",
    "social_django",
    "django_otp",
]
```

---

## 🔑 3. JWT & Cookie Authentication Flow

Recommended: **Access Token in memory + Refresh Token in httpOnly cookie**.

### Login View Sketch

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .tokens import get_tokens_for_user
from django.conf import settings

@api_view(["POST"])
@permission_classes([AllowAny])
def token_obtain_pair_cookie(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]

    if user.two_factor.enabled:
        return Response({"detail": "2FA required"}, status=status.HTTP_403_FORBIDDEN)

    tokens = get_tokens_for_user(user)
    response = Response({"access": tokens["access"]}, status=status.HTTP_200_OK)
    response.set_cookie(
        key="refresh",
        value=tokens["refresh"],
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
        max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
    )
    return response
```

### Refresh & Logout

```python
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def token_refresh_cookie(request):
    refresh_token = request.COOKIES.get("refresh")
    if not refresh_token:
        return Response({"detail": "Refresh token missing."}, status=401)
    serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
    serializer.is_valid(raise_exception=True)
    new_access = serializer.validated_data["access"]
    response = Response({"access": new_access})
    if "refresh" in serializer.validated_data:
        response.set_cookie(
            key="refresh", value=serializer.validated_data["refresh"], httponly=True, secure=not settings.DEBUG
        )
    return response

@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    refresh_token = request.COOKIES.get("refresh")
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass
    response = Response({"detail": "Logged out."}, status=200)
    response.delete_cookie("refresh")
    return response
```

---

## 🛡️ 4. Two-Factor Authentication (TOTP)

*Generate TOTP, QR codes, and verify tokens.*

```python
import pyotp, qrcode, io, base64
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

class TwoFactorViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=["get"])
    def setup(self, request):
        secret = request.user.generate_2fa_secret()
        otpauth_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=request.user.email, issuer_name="AuthProj")
        img = qrcode.make(otpauth_uri)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_b64 = base64.b64encode(buf.getvalue()).decode()
        return Response({"qr_b64": qr_b64, "secret": secret})

    @action(detail=False, methods=["post"])
    def enable(self, request):
        token = request.data.get("token")
        totp = pyotp.TOTP(request.user.two_factor.secret)
        if not totp.verify(token, valid_window=1):
            return Response({"detail": "Invalid TOTP token"}, status=400)
        backup_codes = request.user.two_factor.generate_backup_codes()
        request.user.two_factor.enabled = True
        request.user.two_factor.save()
        return Response({"detail": "2FA enabled.", "backup_codes": backup_codes})
```

---

## 🔗 5. OAuth2 / OIDC (Social Login)

* Use `social-auth-app-django`
* Pipeline ensures **verified email** only

```python
# accounts/pipeline.py
from social_core.exceptions import AuthForbidden

def require_verified_email(backend, details, response, *args, **kwargs):
    if not details.get("email_verified", False):
        raise AuthForbidden(backend)
```

* **Account Linking:** Use `associate_by_email` in the pipeline
* **Security Note:** Require password before linking social accounts for sensitive apps

---

## 🏠 6. Multi-Tenant Authentication

**Row-Level Security** approach:

* Inject `tenant_id` in JWT
* Middleware resolves tenant by subdomain/header
* Enforce `request.tenant` checks on all resources

```python
# accounts/middleware.py
class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        # request.tenant = Tenant.objects.get(domain=host)
        response = self.get_response(request)
        return response
```

---

## 🧪 7. Testing & Hardening Checklist

**Testing Strategy**

| Type        | Focus                                       | Example                                          |
| ----------- | ------------------------------------------- | ------------------------------------------------ |
| Unit        | Serializers, 2FA, token generation          | Ensure LoginSerializer rejects unverified emails |
| Integration | Register → Activate → Login → Token refresh | Simulate cookie-based SPA login                  |
| Security    | Rate limiting, blacklisted tokens           | Attempt to use revoked refresh token             |

**Operational Hardening**

| Security Item   | Action                            | Tool/Library                |
| --------------- | --------------------------------- | --------------------------- |
| Rate Limiting   | Limit POST attempts               | `django-axes` / API Gateway |
| Logging         | Auth events (success/failure/2FA) | ELK / CloudWatch            |
| Key Rotation    | Rotate JWT signing keys regularly | CI/CD pipeline              |
| Email           | Reliable SMTP with DKIM/SPF       | SendGrid / AWS SES / Celery |
| Dependency Scan | Monitor CVEs                      | Dependabot / SNYK           |
| DB Encryption   | Encrypt `TwoFactor.secret`        | `django-cryptography`       |

---

## 💡 8. Summary Recommendations

* Use **Session Auth** for Django Admin and **JWT** for APIs
* **Never** store refresh tokens in localStorage—use **HTTP-only cookies**
* Offload email tasks to **background workers** (Celery/RQ)
* Abstract 2FA and token logic into **services/utilities** instead of views



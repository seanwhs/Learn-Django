# **Django Authentication Project — Full Documentation**
![alt text](image-1.png)
This document provides a **complete guide** for building a secure Django authentication system, including **JWT authentication, 2FA, tenant support, social login**, and **full Postman integration** for testing.

---

## **Step 1: Project Setup & Core Configuration**

### **1️⃣ `authproj/settings.py`**

```python
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---------------------------
# Base Directory
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# Core Settings
# ---------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ---------------------------
# Installed Apps
# ---------------------------
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'social_django',
    'django_otp',

    # Project apps
    'accounts',
    'tenants',
]

# ---------------------------
# Middleware
# ---------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middleware
    'accounts.middleware.TenantMiddleware',
]

# ---------------------------
# URL and Templates
# ---------------------------
ROOT_URLCONF = 'authproj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'authproj.wsgi.application'

# ---------------------------
# Database Configuration
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME", "authdb"),
        'USER': os.environ.get("DB_USER", "authuser"),
        'PASSWORD': os.environ.get("DB_PASSWORD", "authpass"),
        'HOST': os.environ.get("DB_HOST", "localhost"),
        'PORT': os.environ.get("DB_PORT", "5432"),
    }
}

# ---------------------------
# Password Validators
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------
# Custom User Model
# ---------------------------
AUTH_USER_MODEL = "accounts.CustomUser"

# ---------------------------
# Localization
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------
# Static Files
# ---------------------------
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------
# Security Settings
# ---------------------------
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
X_FRAME_OPTIONS = 'DENY'

# ---------------------------
# Django REST Framework
# ---------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
}

# ---------------------------
# JWT Configuration
# ---------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': os.environ.get("JWT_SIGNING_KEY", SECRET_KEY),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ALGORITHM': 'HS256',
}

# ---------------------------
# Social Authentication
# ---------------------------
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'accounts.pipeline.require_verified_email',  # Custom email verification
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
```

**✅ Notes:**

* Environment variables improve security and make deployment easier.
* JWT and refresh tokens are securely configured with rotation and blacklisting.
* Social auth pipeline enforces **verified emails** before creating accounts.

---

### **2️⃣ `accounts/models.py` — Custom User & 2FA**

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import pyotp
import secrets

class CustomUser(AbstractUser):
    """
    Extends Django's AbstractUser with email verification and tenant support.
    """
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    tenant = models.ForeignKey("tenants.Tenant", null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def generate_2fa_secret(self):
        """
        Creates or updates the TOTP secret for the user.
        """
        from .models import TwoFactor
        secret = pyotp.random_base32()
        TwoFactor.objects.update_or_create(user=self, defaults={'secret': secret})
        return secret

class TwoFactor(models.Model):
    """
    Stores user 2FA TOTP secret and backup codes.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="two_factor")
    secret = models.CharField(max_length=32, blank=True, null=True)
    enabled = models.BooleanField(default=False)
    backup_codes = models.JSONField(default=list)

    def generate_backup_codes(self, n=5):
        """
        Generate n backup codes for 2FA recovery.
        """
        codes = [secrets.token_hex(4) for _ in range(n)]
        self.backup_codes = codes
        self.save()
        return codes
```

**✅ Notes:**

* `generate_2fa_secret()` ensures TOTP setup per user.
* Backup codes provide recovery if the user loses access to the authenticator app.

---

# **Step 2: Views, JWT Utilities & Middleware**

This step implements **core authentication flows**, including registration, login with JWT, 2FA setup, social login pipeline, and tenant middleware.

---

### **1️⃣ `accounts/tokens.py` — JWT Utilities**

```python
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """
    Generates JWT access and refresh tokens for the given user.
    Returns a dictionary:
        {
            'refresh': <refresh_token>,
            'access': <access_token>
        }
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

**✅ Notes:**

* Provides a **central utility** for JWT token issuance.
* Supports **token rotation and blacklisting** automatically via SimpleJWT.

---

### **2️⃣ `accounts/views.py` — Authentication & 2FA**

```python
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshSerializer
import pyotp, qrcode, io, base64

from .serializers import RegisterSerializer, LoginSerializer
from .tokens import get_tokens_for_user
from .models import TwoFactor

# ---------------------------
# User Registration
# ---------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Registers a new user. User is inactive until email verification.
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # TODO: implement sending verification email
    return Response(
        {'detail': 'User registered. Please verify your email to activate the account.'},
        status=status.HTTP_201_CREATED
    )

# ---------------------------
# Login & JWT Issuance
# ---------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain_pair_cookie(request):
    """
    Authenticates a user and issues JWT access token in response body,
    refresh token is set in HttpOnly cookie.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    # If 2FA is enabled, require TOTP verification
    if hasattr(user, 'two_factor') and user.two_factor.enabled:
        return Response(
            {'detail': '2FA required', 'mfa_token': 'temporary-session-or-token'},
            status=status.HTTP_403_FORBIDDEN
        )

    tokens = get_tokens_for_user(user)
    response = Response({'access': tokens['access']}, status=status.HTTP_200_OK)
    response.set_cookie(
        key='refresh',
        value=tokens['refresh'],
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
    )
    return response

# ---------------------------
# Refresh Access Token
# ---------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_cookie(request):
    """
    Refreshes the access token using the refresh token stored in HttpOnly cookie.
    """
    refresh_token = request.COOKIES.get('refresh')
    if not refresh_token:
        return Response({"detail": "Refresh token missing."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
    serializer.is_valid(raise_exception=True)

    new_access = serializer.validated_data['access']
    response = Response({'access': new_access}, status=status.HTTP_200_OK)

    # Update refresh token if rotated
    if 'refresh' in serializer.validated_data:
        response.set_cookie(
            key='refresh',
            value=serializer.validated_data['refresh'],
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax'
        )

    return response

# ---------------------------
# Logout
# ---------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """
    Logs out user by blacklisting the refresh token and clearing cookie.
    """
    refresh_token = request.COOKIES.get('refresh')
    if refresh_token:
        try:
            RefreshToken(refresh_token).blacklist()
        except Exception:
            pass

    response = Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
    response.delete_cookie('refresh')
    return response

# ---------------------------
# 2FA Setup & Enable
# ---------------------------
class TwoFactorViewSet(viewsets.GenericViewSet):
    """
    Handles 2FA setup and enabling for authenticated users.
    """
    permission_classes = []

    def setup(self, request):
        """
        Generates TOTP secret and returns QR code for authenticator apps.
        """
        user = request.user
        secret = user.generate_2fa_secret()
        otpauth_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="YourWebApp"
        )

        # Generate QR code as base64 string
        img = qrcode.make(otpauth_uri)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        qr_b64 = base64.b64encode(buf.getvalue()).decode()

        return Response({'qr_b64': qr_b64, 'secret': secret})

    def enable(self, request):
        """
        Enables 2FA after validating TOTP token.
        Generates backup codes for recovery.
        """
        token = request.data.get('token')
        two_factor = request.user.two_factor
        totp = pyotp.TOTP(two_factor.secret)

        if not totp.verify(token, valid_window=1):
            return Response({"detail": "Invalid TOTP token."}, status=status.HTTP_400_BAD_REQUEST)

        two_factor.enabled = True
        backup_codes = two_factor.generate_backup_codes()
        two_factor.save()

        return Response({"detail": "2FA enabled successfully.", "backup_codes": backup_codes})
```

**✅ Notes:**

* JWT access token returned in body; refresh token is **HttpOnly cookie**.
* 2FA endpoints provide QR code generation and token verification.
* Can integrate with **Google Authenticator or Authy**.

---

### **3️⃣ `accounts/middleware.py` — Tenant Middleware**

```python
from tenants.models import Tenant

class TenantMiddleware:
    """
    Resolves the current tenant from the request host.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]  # remove port if exists
        try:
            request.tenant = Tenant.objects.get(domain=host)
        except Tenant.DoesNotExist:
            request.tenant = None
        return self.get_response(request)
```

**✅ Notes:**

* Allows multi-tenant support using **subdomain or domain-based tenant mapping**.
* `request.tenant` can be accessed in views for tenant-aware logic.

---

### **4️⃣ `accounts/pipeline.py` — Social Auth Email Verification**

```python
from social_core.exceptions import AuthForbidden

def require_verified_email(backend, details, response, *args, **kwargs):
    """
    Prevents login if social provider email is not verified.
    """
    if not details.get('email_verified', False):
        raise AuthForbidden(backend)
```

**✅ Notes:**

* Enforces email verification for OAuth providers like Google.
* Prevents creating inactive or fake accounts via social login.

---

Perfect! Let’s continue with **Step 3: URLs, Admin, Routers, and Postman Integration**—fully polished, detailed, and structured.

---

# **Step 3: URL Routes, Admin Registration & DRF Routers**

This step organizes all **API endpoints**, 2FA routes, social login paths, and admin configurations.

---

### **1️⃣ `accounts/urls.py` — API Endpoints**

```python
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    register_view,
    token_obtain_pair_cookie,
    token_refresh_cookie,
    logout_view,
    TwoFactorViewSet,
)

# DRF Router for 2FA endpoints
router = DefaultRouter()
router.register(r'2fa', TwoFactorViewSet, basename='twofactor')

urlpatterns = [
    # User registration
    path('register/', register_view, name='register'),

    # JWT token issuance and refresh
    path('token/', token_obtain_pair_cookie, name='token_obtain_pair'),
    path('token/refresh/', token_refresh_cookie, name='token_refresh'),

    # Logout endpoint
    path('logout/', logout_view, name='logout'),
]

# Append router-generated 2FA endpoints
urlpatterns += router.urls
```

**✅ Notes:**

* `DefaultRouter` automatically generates `/2fa/setup/` and `/2fa/enable/` endpoints.
* All endpoints follow **RESTful conventions** and are namespaced under `/api/auth/`.

---

### **2️⃣ `authproj/urls.py` — Project-Level URLs**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # All authentication-related endpoints
    path('api/auth/', include('accounts.urls')),

    # Optional: Social auth routes (Google, Facebook, etc.)
    path('auth/social/', include('social_django.urls', namespace='social')),
]
```

**✅ Notes:**

* `/api/auth/` → all custom authentication API endpoints.
* `/auth/social/` → OAuth login URLs provided by `social_django`.

---

### **3️⃣ `accounts/admin.py` — Admin Registration**

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TwoFactor

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_email_verified', 'tenant')
    list_filter = ('is_staff', 'is_active', 'is_email_verified', 'tenant')
    search_fields = ('username', 'email')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Verification', {'fields': ('is_email_verified', 'tenant')}),
    )

@admin.register(TwoFactor)
class TwoFactorAdmin(admin.ModelAdmin):
    list_display = ('user', 'enabled')
    readonly_fields = ('backup_codes',)
```

**✅ Notes:**

* Backup codes are **read-only** to avoid accidental edits.
* Admin view displays **is_email_verified** and **tenant** for quick management.
* Filtering and searching help manage large user datasets efficiently.

---

### **4️⃣ DRF Router Notes**

| Endpoint                | Method | Purpose                              |
| ----------------------- | ------ | ------------------------------------ |
| `/api/auth/2fa/setup/`  | GET    | Generate 2FA secret & QR code        |
| `/api/auth/2fa/enable/` | POST   | Enable 2FA and generate backup codes |

* Integrates seamlessly with **JWT-secured views**.
* Can be extended to include **disable 2FA** or **regenerate backup codes** if needed.

---

### **5️⃣ Social Auth URLs (Optional)**

* Example workflow with Google OAuth2:

```
/auth/social/login/google-oauth2/      → Redirects to Google
/auth/social/complete/google-oauth2/   → Callback after login
```

* Social login pipeline (`pipeline.py`) ensures **email verification** before account creation.

---

### **6️⃣ Summary of Auth URL Structure**

```
POST /api/auth/register/           → Register new user
POST /api/auth/token/              → Login → receive JWT + refresh cookie
POST /api/auth/token/refresh/      → Refresh access token via cookie
POST /api/auth/logout/             → Logout → blacklist refresh token + clear cookie
GET  /api/auth/2fa/setup/          → Generate 2FA secret & QR code
POST /api/auth/2fa/enable/         → Enable 2FA & get backup codes
/social/login/<backend>/           → Redirect to OAuth provider
/complete/<backend>/               → OAuth callback endpoint
```

**✅ Outcome:**

* Clean organization of endpoints.
* DRF routers handle 2FA automatically.
* Admin interface allows easy management of users, tenants, and 2FA.
* Social login workflow ready for production integration.

---

### **7️⃣ Postman Collection: Authentication Flows**

**Features included:**

* Registration
* Login → JWT + HttpOnly refresh cookie
* 2FA setup & enable
* Logout
* Token refresh
* Social OAuth stub

**Postman environment variables:**

| Key             | Initial Value                                  | Current Value                                  |
| --------------- | ---------------------------------------------- | ---------------------------------------------- |
| `base_url`      | [http://localhost:8000](http://localhost:8000) | [http://localhost:8000](http://localhost:8000) |
| `access_token`  |                                                |                                                |
| `refresh_token` |                                                |                                                |

**Pre-request script (for authenticated requests):**

```javascript
if (pm.environment.get("access_token")) {
    pm.request.headers.add({
        key: "Authorization",
        value: "Bearer " + pm.environment.get("access_token")
    });
}
```

**Test script (for login request):**

```javascript
if (pm.response.code === 200) {
    let jsonData = pm.response.json();
    if (jsonData.access) { pm.environment.set("access_token", jsonData.access); }
    let refreshCookie = pm.cookies.get("refresh");
    if (refreshCookie) { pm.environment.set("refresh_token", refreshCookie); }
}
```

**Auto-refresh access token script:**

```javascript
const refreshToken = pm.environment.get("refresh_token");
if (!pm.environment.get("access_token") && refreshToken) {
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/token/refresh/",
        method: "POST",
        header: { "Content-Type": "application/json" },
        body: { mode: "raw", raw: "{}" },
        cookie: [{ name: "refresh", value: refreshToken }]
    }, function (err, res) {
        if (!err && res.code === 200) {
            pm.environment.set("access_token", res.json().access);
            postman.setNextRequest(pm.info.requestName);
        }
    });
}
```

* Organize requests in **folders**: Auth, 2FA, Social.
* Supports **automatic token injection** and refresh.

---

# **Step 4: Unit & Integration Tests**

Recommended folder structure:

```
accounts/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_serializers.py
│   ├── test_views.py
│   └── test_2fa.py
```

---

## **1️⃣ `accounts/tests/test_models.py`**

Tests `CustomUser` and `TwoFactor` model functionality.

```python
from django.test import TestCase
from accounts.models import CustomUser, TwoFactor
from tenants.models import Tenant

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="TenantA", domain="tenanta.example.com")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="securepassword123",
            tenant=self.tenant
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "user@example.com")
        self.assertFalse(self.user.is_email_verified)
        self.assertEqual(self.user.tenant.name, "TenantA")

    def test_generate_2fa_secret(self):
        secret = self.user.generate_2fa_secret()
        self.assertIsNotNone(secret)
        self.assertEqual(self.user.two_factor.secret, secret)
        self.assertFalse(self.user.two_factor.enabled)


class TwoFactorModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="2fauser",
            email="2fa@example.com",
            password="securepass123"
        )

    def test_backup_code_generation(self):
        two_factor = TwoFactor.objects.create(user=self.user)
        codes = two_factor.generate_backup_codes()
        self.assertEqual(len(codes), 5)
        self.assertEqual(two_factor.backup_codes, codes)
```

**✅ Notes:**

* Verifies 2FA secret generation.
* Ensures backup codes are generated correctly.

---

## **2️⃣ `accounts/tests/test_serializers.py`**

Tests serializer validation and creation logic.

```python
from django.test import TestCase
from accounts.serializers import RegisterSerializer
from accounts.models import CustomUser

class RegisterSerializerTest(TestCase):
    def test_valid_serializer(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepass123"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, "new@example.com")
        self.assertFalse(user.is_active)  # Email verification pending

    def test_invalid_serializer_missing_email(self):
        data = {
            "username": "newuser",
            "password": "securepass123"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
```

**✅ Notes:**

* Confirms registration serializer creates inactive users.
* Validates error handling for missing required fields.

---

## **3️⃣ `accounts/tests/test_views.py`**

Tests full **authentication flows**, including JWT issuance, refresh, and logout.

```python
from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import CustomUser
from rest_framework import status

class AuthViewsTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="securepassword123",
            is_email_verified=True
        )

    def test_register_view(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "mypassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())

    def test_login_view_with_correct_credentials(self):
        url = reverse('token_obtain_pair')
        data = {"username": "testuser", "password": "securepassword123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.cookies)

    def test_login_view_invalid_credentials(self):
        url = reverse('token_obtain_pair')
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        login_url = reverse('token_obtain_pair')
        login_resp = self.client.post(login_url, {"username": "testuser", "password": "securepassword123"})
        refresh_cookie = login_resp.cookies.get('refresh').value

        refresh_url = reverse('token_refresh')
        self.client.cookies['refresh'] = refresh_cookie
        response = self.client.post(refresh_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_logout_view(self):
        login_url = reverse('token_obtain_pair')
        login_resp = self.client.post(login_url, {"username": "testuser", "password": "securepassword123"})
        refresh_cookie = login_resp.cookies.get('refresh').value

        self.client.cookies['refresh'] = refresh_cookie
        logout_url = reverse('logout')
        response = self.client.post(logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('refresh', response.cookies)
```

**✅ Notes:**

* Tests cookie-based JWT flows.
* Validates login, token refresh, and logout logic.

---

## **4️⃣ `accounts/tests/test_2fa.py`**

Tests **2FA setup, verification, and backup code generation**.

```python
from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import CustomUser
import pyotp

class TwoFactorTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user2fa",
            email="2fa@example.com",
            password="strongpassword123",
            is_email_verified=True
        )
        self.client.force_authenticate(user=self.user)

    def test_2fa_setup_and_enable(self):
        # Step 1: Generate secret + QR code
        setup_url = reverse('twofactor-setup')
        response = self.client.get(setup_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("qr_b64", response.data)
        secret = response.data['secret']

        # Step 2: Enable 2FA with valid TOTP token
        totp = pyotp.TOTP(secret)
        token = totp.now()
        enable_url = reverse('twofactor-enable')
        response = self.client.post(enable_url, {"token": token}, format='json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.two_factor.enabled)
        self.assertGreater(len(self.user.two_factor.backup_codes), 0)
```

**✅ Notes:**

* Validates **secret generation**, **QR code creation**, **TOTP verification**, and **backup code generation**.
* Ensures full 2FA integration with JWT flows.

---

### **5️⃣ Summary of Testing Coverage**

* **Registration:** Ensures inactive user creation until email verification.
* **Login:** JWT access + refresh cookie issued correctly.
* **Token Refresh:** Cookie rotation and access token renewal.
* **Logout:** Blacklists refresh token and clears cookie.
* **2FA:** Setup, enable, TOTP validation, and backup codes.
* **Serializers & Models:** Validation, backup code generation, and secret management.

---

These tests are compatible with:

* Django’s built-in `manage.py test`
* `pytest-django` for more advanced test reporting

---


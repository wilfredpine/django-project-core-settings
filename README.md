# django-project-core-settings

**Production-ready, modular, and secure Django settings package.**

This package provides a clean, maintainable, and highly secure base configuration for Django projects. It follows Django best practices and OWASP recommendations, making it easy to start new projects with strong security defaults.

## Features

- **Fully environment-driven** configuration using `.env`
- **Modular architecture** — settings split into logical components
- **Multiple environments** support: `dev`, `prod`, and `local`
- **Strong security defaults**:
  - HSTS with preload
  - Secure cookies (`HttpOnly`, `SameSite=Strict`)
  - CSP (Content Security Policy)
  - Argon2 password hashing
  - Brute-force protection (`django-axes`)
  - Rate limiting (`django-ratelimit`)
- **Structured JSON logging** (app, security, and error logs)
- **WhiteNoise** integration for static files
- **Redis cache** support
- **Easy extensibility** via `EXTRA_INSTALLED_APPS` and `EXTRA_MIDDLEWARE`
- **DID_AUTH** ready (custom authentication app) (`https://pypi.org/project/django-did-auth/`)

## Installation

```bash
pip install django-project-core-settings
```

## Create Django Project

```bash
django-admin startproject myproject
```

## create user app

```bash
py manage.py startapp users
```

- create custom user model at `users/models.py`


### Sample custom model

- `your_project/users/models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)
class CustomUser(AbstractUser):
    username = None
    # Role choices (easy to extend)
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('staff', 'Staff Member'),
        ('moderator', 'Moderator'),
        ('user', 'Regular User'),
    ]
    # Core fields
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    # Role & profile
    role = models.CharField(
        _('role'), 
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='user',
        db_index=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Will be False until email verified
    date_joined = models.DateTimeField(default=timezone.now)
    activation_token_created = models.DateTimeField(
        _('activation token created'),
        null=True,
        blank=True
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    def __str__(self):
        return self.email
```

# Quick Start

Create your project settings file:

```python
# myproject/settings.py
from django_project_core_settings import *

from django_project_core_settings.utils.env import get_list_env

# === Extend with your apps ===
INSTALLED_APPS += [
    'users', # register your user app
    # 'blog',
    # 'portfolio',
    # 'ckeditor',
]

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE += [
    # 'your.middleware.Class',
]

# === Common overrides ===
# LOGIN_REDIRECT_URL = '/dashboard/' # already in DID_AUTH
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# === Security & Domain ===
ALLOWED_HOSTS = get_list_env("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])

# Add frontend domains if needed
CSRF_TRUSTED_ORIGINS += [
    "https://your-frontend.com",
]

if get_list_env("DJANGO_ENV") == "prod" or get_list_env("DJANGO_ENV") == "local" :
    CORS_ALLOWED_ORIGINS = [
        "https://yourdomain.com",
    ]

# === default DID_AUTH config (can be overridden in dev/prod) ===
# https://pypi.org/project/django-did-auth/
DID_AUTH = {
    # "LOGIN_REDIRECT": "/dashboard/", # already redirect based on the roles below
    "LOGOUT_REDIRECT": "/login/",
    
    "ADMIN_URL": "admin/",
    "ADMIN_IP_WHITELIST": get_list_env("ADMIN_IP_WHITELIST", default=['127.0.0.1', '::1']),  # Localhost by default

    # on your URL
    # from django_did_auth.config.loader import get_admin_url
    # urlpatterns = [
    #     path(get_admin_url(), admin.site.urls),
    # ]

    # redirect based on roles
    "ROLES": { 
        "admin": "/admin-dashboard/",
        "staff": "/staff-dashboard/",
        "moderator": "/moderator-dashboard/",
        "user": "/dashboard/",
    },
    # make sure it matches your models.py roles
    # ROLE_CHOICES = [
    #     ('admin', 'Administrator'),
    #     ('user', 'Regular User'),
    # ]

    "DENY_BEHAVIOR": "redirect",  # or "forbidden"

    "EMAIL": {
        "VERIFY_EXPIRY_HOURS": 24,
        "RESET_EXPIRY_HOURS": 1,
        "FROM_EMAIL": None,  # Will use DEFAULT_FROM_EMAIL
    },

    "RATE_LIMIT": {
        "LOGIN": "10/m",
        "REGISTER": "5/m",
        "PASSWORD_RESET": "5/m",
    },

    "UI_FRAMEWORK": "tailwind",  # "tailwind" or "bootstrap"

    "ENABLE_AUDIT": True,
    "TRUST_PROXY": False,
    
    "SECURITY": {
        "PASSWORD_MIN_LENGTH": 12,
        "ENABLE_AXES": True,
        "LOCKOUT_AFTER_ATTEMPTS": 5,
        "LOCKOUT_DURATION_MINUTES": 30,
        "REQUIRE_HTTPS": True,          # Enforce in production
    },
    "AUDIT": {
        "ENABLED": True,
        "LOG_SENSITIVE": False,         # Don't log passwords
    }
    
}
# === DID_AUTH Customization ===
# DID_AUTH['ROLES'].update({
#     'editor': '/dashboard/editor/',
#     'author': '/dashboard/author/',
# })
# make sure it matches your models.py roles
# ROLE_CHOICES = [
#     ('editor', 'Editor'),
#     ('author', 'Author'),
# ]


# Additinal settings can be added here as needed
# E.g.
# Admin security
MIDDLEWARE.insert(0, 'django_did_auth.security.admin.ipwhitelist.AdminIPWhitelistMiddleware')


```

## Short Example

```python
from django_project_core_settings import *
from django_project_core_settings.utils.env import get_list_env
# === Extend with your apps ===
INSTALLED_APPS += [
    # Third-party
    # Local apps
    'accounts',
]
AUTH_USER_MODEL = 'accounts.CustomUser'
MIDDLEWARE += [
    # 'your.middleware.Class',
]
ROOT_URLCONF = 'core_system.urls'
WSGI_APPLICATION = 'core_system.wsgi.application'
ALLOWED_HOSTS = get_list_env("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS += [
    "https://your-frontend.com",
]
if get_list_env("DJANGO_ENV") == "prod" or get_list_env("DJANGO_ENV") == "local" :
    CORS_ALLOWED_ORIGINS = [
        "https://yourdomain.com",
    ]
DID_AUTH = {
    "LOGOUT_REDIRECT": "/auth/login/",
    "ADMIN_URL": "secret-admin/",
    "ADMIN_IP_WHITELIST": get_list_env("ADMIN_IP_WHITELIST", default=['127.0.0.1', '::1']),
    # redirect based on roles
    "ROLES": {
        "owner": "/dashboard/owner/",
        "manager": "/dashboard/manager/",
        "staff": "/dashboard/staff/",
    },
    "DENY_BEHAVIOR": "forbidden",  # or "redirect"
}
# Admin security
MIDDLEWARE.insert(0, 'django_did_auth.security.admin.ipwhitelist.AdminIPWhitelistMiddleware')
```

## Environment Variables (.env)

```env
# Django environment variables (for development, local, and production)
# dev | prod | local
DJANGO_ENV=dev

# Secret key (replace with your own secure key in production)
# Always rotate this key periodically and keep it secret. Do not hardcode it in your codebase; use environment variables instead.
# You can generate a secure key using Django's get_random_secret_key() function or an online generator.
# Example: from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())
# For development, you can use a hardcoded key, but make sure to change it for production and keep it secret.
# Never commit your actual secret key to version control. Use environment variables or a secrets manager in production.
# Add .env in .gitignore to prevent it from being committed.
SECRET_KEY='your-secret-key'

# Comma-separated list of allowed hosts (e.g., localhost,
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Email settings (using Gmail SMTP as an example)
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password

# Optional: restrict admin access to specific IPs (comma-separated list)
ADMIN_IP_WHITELIST=192.168.68.100,

# Enable or disable the REST API (set to true to enable)
# if true, it will load the custom secured rest_api settings, otherwise it will skip it.
# Set true if you want to use API
ENABLE_REST_API=true 
# JWT key for signing tokens (replace with your own secure key in production)
# Must be a 256-bit key (32 bytes) for HS256 algorithm. You can generate one using a secure random generator.
# Example: openssl rand -hex 32
# Always rotate this key periodically and keep it secret. Do not hardcode it in your codebase; use environment variables instead.
JWT_SIGNING_KEY=your-256-bit-secret-key-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Add your frontend URL here (e.g., http://localhost:3000 for React dev server)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://yourdomain.com
CORS_ALLOWED_ORIGINS=http://127.0.0.1:5500/,http://127.0.0.1:8000/

# Redis settings (for caching, rate limiting, and lockout)
REDIS_REQUIRED=True # required True for prod
REDIS_URL=redis://127.0.0.1:6379/1

# ----------------------------------------------------------------------------------------------------
# Default values for rate limiting and lockout (can be overridden by environment variables)
# ----------------------------------------------------------------------------------------------------

## Lockout settings for django-axes

# AXES_FAILURE_LIMIT = 5
# AXES_COOLOFF_TIME = 30 # in minutes

## Rate limit settings for django-ratelimit 

# LOGIN_RATE=10/m
# REGISTER_RATE=5/m
# PASSWORD_RESET_RATE=5/m

## Custom rate limits for different API endpoints

# API_PUBLIC_READONLY_RATE=200/min
# PUBLIC_GET_RATE=200/min
# PUBLIC_POST_RATE=50/min
# API_KEY_RATE=200/min
# API_PUBLIC_RATE=100/min
# API_AUTHENTICATED_RATE=1000/min
# LOGIN_IP_RATE=10/min
# LOGIN_EMAIL_RATE=5/min
# REGISTER_IP_RATE=5/min
# REGISTER_EMAIL_RATE=3/min
# PASSWORD_RESET_REQUEST_RATE=5/min
# PASSWORD_RESET_CONFIRM_RATE=5/min
# CHANGE_PASSWORD_RATE=10/min
```

## Run Commands

```bash
# Development
DJANGO_ENV=dev python manage.py runserver

# Production check
DJANGO_ENV=prod python manage.py check

# Local development with debug tools
DJANGO_ENV=local python manage.py runserver
```

## What You Can Override

### Safe to override:

- `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`
- `DID_AUTH['ROLES']`
- `LOGIN_REDIRECT_URL`, `ROOT_URLCONF`, etc.

### Do NOT override directly:

- `SECRET_KEY`
- `AUTHENTICATION_BACKENDS`
- Core security headers (HSTS, secure cookies, etc.)
- `MIDDLEWARE` and `INSTALLED_APPS` base lists (use `MIDDLEWARE += []`, `INSTALLED_APPS += []` instead)


## Logging
The package provides three log files in the `logs/` directory:

- `app.log` — General application logs
- `security.log` — Authentication, rate limiting, and security events (JSON in production)
- `error.log` — Error tracking

### Requirements

```bash
dependencies = [
    "Django>=4.2",
    "python-dotenv>=1.0",
    "whitenoise>=6.0",
    "django-axes>=6.0",
    "django-ratelimit>=4.0",
    "django-redis>=5.0",
    "python-json-logger>=2.0",
    "django-did-auth>=0.1",
]
```

- Use `pip install django-debug-toolbar` for local (`DJANGO_ENV=local`)


---


### From Django-DID-Auth (A secure, pluggable authentication framework for Django)

---

## Role-Based Redirection Settings (already in Settings above)

```python
DID_AUTH = {
    "ROLES": {
        "admin": "/dashboard/admin/",
        "staff": "/dashboard/staff/",
        "user": "/dashboard/",
    }
}
```

## Activate on project URL


#### Using full authentication:
- `your_project/urls.py`

```python

from django.views.generic.base import RedirectView
from django_did_auth.core.views.password import change_password_view

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # DID_AUTH URLs
    path('auth/', include('django_did_auth.urls')), # Include DID_AUTH URLs
    path('', RedirectView.as_view(pattern_name='did_auth:login', permanent=False)),
    path('profile/change-password/', change_password_view, name="change_password"), 

    # 👤 Role Dashboards
    path('dashboard/admin/', main_views.admin_dashboard),
    path('dashboard/', main_views.user_dashboard),
]
```

#### Or using only specific authentication:

- create `urls.py` at your app where custom_user model made
- Example: `your_project/user_app/urls.py`

```python

from django.urls import path
from django.shortcuts import render
from django_did_auth.core.views.register import register_view
from django_did_auth.core.views.login import login_view
from django_did_auth.core.views.logout import logout_view
from django_did_auth.core.views.activation import activate_account_view
from django_did_auth.core.views.password_reset import (
    password_reset_request_view,
    password_reset_confirm_view
)

app_name = "did_auth"

urlpatterns = [
    # Authentication
    # path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Email Verification
    # path("activate/<uidb64>/<token>/", activate_account_view, name="activate"),
    # path("verification-sent/", lambda r: render(r, "did_auth/verification_sent.html"), name="verification_sent"),

    # Password Reset
    # path("password-reset/", password_reset_request_view, name="password_reset_request"),
    # path("password-reset-confirm/<uidb64>/<token>/", password_reset_confirm_view, name="password_reset_confirm"),
]

```

then include it on url project urls
- `your_project/urls.py`

```python
from django.contrib import admin
from django.urls import include, path

from core_system import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_app.urls')), # from `your_project/user_app/urls.py`
    ...
]

```

IMPORTANT: for disabling / or using specific authentication, use custom Templates (see below)


---

## Using Ratelimiter

```python
from django_did_auth.security.ratelimit.decorators import safe_ratelimit

@safe_ratelimit(key='ip', rate="10/m")
@safe_ratelimit(key='post:email', "5/m")
def myform_view(request):
    ...

from django.contrib.auth.decorators import login_required

@login_required
@safe_ratelimit(key="user", rate="5/m", block=True)
def myform_view(request):
    ...
```

---

## Email Integration
- you can use in your project the email sending function using:

```python
from django_did_auth.core.flows.email_flow import send_general_email

send_general_email(
    request,
    user,
    "Welcome!",
    "emails/welcome.html",
    {"name": user.first_name}
)
```

create the `templates/emails/welcome.html`

---

## Audit Logging
- to use the audit log feature inside your project:

```python
from django_did_auth.security.audit.logger import log_event

log_event(request, "login_success", user=request.user)

log_event(
    request=None,
    event="manual_test_error",
    level="error",
    extra={"info": "testing"}
)
```

## Templates Overiding

Create the following files:
- `templates/did_auth/login.html`
```html
<form method="post" class="space-y-6">
    {% csrf_token %}
    <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Email address</label>
        {{ form.email }}
        {% if form.email.errors %}
            <p class="mt-1 text-red-500 text-sm">{{ form.email.errors.0 }}</p>
        {% endif %}
    </div>
    <div>
        <div class="flex justify-between items-center">
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <a href="{% url 'did_auth:password_reset_request' %}" class="text-sm text-blue-600 hover:text-blue-500">Forgot password?</a>
        </div>
        {{ form.password }}
        {% if form.password.errors %}
            <p class="mt-1 text-red-500 text-sm">{{ form.password.errors.0 }}</p>
        {% endif %}
    </div>
    <button type="submit"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 rounded-2xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
        Sign in
    </button>
</form>
```
- `templates/did_auth/register.html`
```html
<form method="post" class="space-y-6">
    {% csrf_token %}
    <div class="grid grid-cols-2 gap-4">
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">First name</label>
            {{ form.first_name }}
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Last name</label>
            {{ form.last_name }}
        </div>
    </div>
    <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Email address</label>
        {{ form.email }}
    </div>
    <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
        {{ form.password1 }}
    </div>
    <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Confirm password</label>
        {{ form.password2 }}
    </div>
    <button type="submit"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3.5 rounded-2xl transition-all duration-200">
        Create account
    </button>
</form>
```
- `templates/did_auth/lockout.html`
```html
<div class="text-center py-12 space-y-6">
    <h2 class="text-3xl font-bold text-red-600">Account Temporarily Locked</h2>
    <p class="text-gray-600">Too many failed login attempts from this IP or account.</p>
    <p>Please try again later or contact support.</p>
    
    <a href="{% url 'did_auth:login' %}" 
       class="inline-block px-6 py-3 bg-gray-800 text-white rounded-2xl hover:bg-gray-900">
        Back to Login
    </a>
</div>
```
- `templates/did_auth/password_reset_confirm.html`
```html
{% if valid_link and form %}
    <form method="post" class="space-y-6">
        {% csrf_token %}
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">New password</label>
            {{ form.new_password }}
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Confirm new password</label>
            {{ form.confirm_password }}
        </div>
        <button type="submit"
                class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3.5 rounded-2xl">
            Reset password
        </button>
    </form>
{% else %}
    <div class="text-center text-red-600 py-8">
        This password reset link is invalid or has expired.
    </div>
    <a href="{% url 'did_auth:password_reset_request' %}" 
        class="block text-center text-blue-600 hover:text-blue-500">
        Request a new reset link
    </a>
{% endif %}
```
- `templates/did_auth/password_reset_request.html`
```html
<form method="post" class="space-y-6">
    {% csrf_token %}
    <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Email address</label>
        {{ form.email }}
    </div>
    <button type="submit"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3.5 rounded-2xl transition-all">
        Send reset link
    </button>
</form>
```
- `templates/did_auth/verification_sent.html`
```html
<h2 class="text-3xl font-semibold text-gray-900">Check your email</h2>
<p class="text-gray-600 max-w-sm mx-auto">
    We've sent a verification link to your email address. 
    Please click the link to activate your account.
</p>
```
- `templates/did_auth/email/activation.html`
```html
<h2>Hi {{ user.first_name|default:user.email }},</h2>
<p>Thank you for registering! Please click the button below to activate your account:</p>
<a href="{{ activation_link }}" 
    style="display: inline-block; background: #4f46e5; color: white; padding: 14px 28px; 
            text-decoration: none; border-radius: 8px; font-weight: 600; margin: 20px 0;">
    Activate My Account
</a>
<p style="color: #666; font-size: 0.95rem;">
    This link will expire in {{ expiry|default:24 }} hours.
</p>
```
- `templates/did_auth/email/password_reset.html`
```html
<h2>Hi {{ user.first_name|default:user.email }},</h2>
<p>You requested a password reset. Click the link below to set a new password:</p>
<a href="{{ reset_link }}" 
    style="display: inline-block; background: #4f46e5; color: white; padding: 14px 28px; 
            text-decoration: none; border-radius: 8px; font-weight: 600; margin: 20px 0;">
    Reset My Password
</a>
<p style="color: #666;">This link will expire soon.</p>
<p>If you didn't request this, please ignore this email.</p>
```
- `templates/profile/change_password.html`
```html
<form method="post">
    {% csrf_token %}
    {{ form.non_field_errors }}
    <div class="space-y-4">
        {{ form.current_password.label_tag }}
        {{ form.current_password }}

        {{ form.new_password.label_tag }}
        {{ form.new_password }}

        {{ form.confirm_password.label_tag }}
        {{ form.confirm_password }}
    </div>
    <button class="mt-6 w-full bg-blue-600 text-white py-2 rounded">
        Update Password
    </button>
</form>
```

---

## Sample custom model
- `your_project/users/models.py`

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)
class CustomUser(AbstractUser):
    username = None
    # Role choices (easy to extend)
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('staff', 'Staff Member'),
        ('moderator', 'Moderator'),
        ('user', 'Regular User'),
    ]
    # Core fields
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    # Role & profile
    role = models.CharField(
        _('role'), 
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='user',
        db_index=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Will be False until email verified
    date_joined = models.DateTimeField(default=timezone.now)
    activation_token_created = models.DateTimeField(
        _('activation token created'),
        null=True,
        blank=True
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    def __str__(self):
        return self.email
```

## Re-used Register flow on your `Views`

```python
from django_did_auth.core.flows.register_flow import register_user

if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            user = register_user(request, form)
```

- this will save as `user.is_active = False`


## Role-aware Access Control

```python
from django_did_auth.security.decorators.roles import role_required

@role_required("owner") # Supported: @role_required("admin", "owner")
def dashboard(request):
    ...
```

If user is:
- ✅ owner → allow
- ❌ not owner → redirect or forbidden
if you have `DID_AUTH["DENY_BEHAVIOR"] = "redirect",` in settings it redirect to their dashboard, if `DID_AUTH["DENY_BEHAVIOR"] = "forbidden",` in setting it show error 403 instead

---

# How to use handler404

## In PROJECT `urls.py`
```python
handler404 = "django_did_auth.core.utils.errors.handle_404"
```

---

# Overried Error Templates

## Template override only
Create the following templates
- `Templates/did_auth/errors/401.html`


```html
<div class="bg-white shadow-lg rounded-2xl p-8 max-w-md text-center">
    <div class="text-red-500 text-6xl font-bold">401</div>
    <h1 class="text-2xl font-semibold mt-4 text-gray-800">
        Authentication Required
    </h1>
    <p class="text-gray-600 mt-2">
       {{ message|default:"You do not have permission." }}
    </p>
    <p class="text-sm text-gray-400 mt-3">
        If you believe this is an error, contact your administrator.
    </p>
    <a href="/" 
       class="inline-block mt-6 px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        Go Home
    </a>
</div>
```
- `Templates/did_auth/errors/403.html`

```html
<div class="bg-white shadow-lg rounded-2xl p-8 max-w-md text-center">
    <div class="text-red-500 text-6xl font-bold">Error 403</div>
    <h1 class="text-2xl font-semibold mt-4 text-gray-800">
        Access Denied
    </h1>
    <p class="text-gray-600 mt-2">
       {{ message|default:"You do not have permission." }}
    </p>
    <p class="text-sm text-gray-400 mt-3">
        If you believe this is an error, contact your administrator.
    </p>
    <a href="/" 
       class="inline-block mt-6 px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        Go Home
    </a>
</div>
```
- `Templates/did_auth/errors/404.html`

```html
<div class="bg-white shadow-lg rounded-2xl p-8 max-w-md text-center">
    <div class="text-red-500 text-6xl font-bold">404</div>
    <h1 class="text-2xl font-semibold mt-4 text-gray-800">
        Page Not Found
    </h1>
    <p class="text-gray-600 mt-2">
       {{ message|default:"You do not have permission." }}
    </p>
    <p class="text-sm text-gray-400 mt-3">
        If you believe this is an error, contact your administrator.
    </p>
    <a href="/" 
       class="inline-block mt-6 px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        Go Home
    </a>
</div>
```
- `Templates/did_auth/errors/423.html`

```html
<div class="bg-white shadow-lg rounded-2xl p-8 max-w-md text-center">
    <div class="text-red-500 text-6xl font-bold">423</div>
    <h1 class="text-2xl font-semibold mt-4 text-gray-800">
        Account Locked
    </h1>
    <p class="text-gray-600 mt-2">
       {{ message|default:"You do not have permission." }}
    </p>
    <p class="text-sm text-gray-400 mt-3">
        If you believe this is an error, contact your administrator.
    </p>
    <a href="/" 
       class="inline-block mt-6 px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        Go Home
    </a>
</div>
```
- `templates/did_auth/errors/429.html`

```html
<div class="bg-white shadow-lg rounded-2xl p-8 max-w-md text-center">
    <div class="text-red-500 text-6xl font-bold">429</div>
    <h1 class="text-2xl font-semibold mt-4 text-gray-800">
        Too Many Requests
    </h1>
    <p class="text-gray-600 mt-2">
       {{ message|default:"You do not have permission." }}
    </p>
    <p class="text-sm text-gray-400 mt-3">
        If you believe this is an error, contact your administrator.
    </p>
    <a href="/" 
       class="inline-block mt-6 px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        Go Home
    </a>
</div>
```

## Other overried technuiqes 
If you don't want to create/overide the html above, in `templates/did_auth/errors/`, then use the approach below:

- Add in `settings.py` (SETTINGS — PLUGGABLE OVERRIDE)

```python
DID_AUTH["ERROR_HANDLERS"] = {
        "403": "myproject.errors.custom_403",
        "404": "myproject.errors.custom_404",
        "429": "myproject.errors.custom_429",
    }
```

- PROJECT OVERRIDE EXAMPLE (`myproject/errors.py`)
```python
from django.shortcuts import render

def custom_403(request, message=None):
    return render(request, "custom/403.html", {"message": message}, status=403)
```

How it works
```bash
role_required()
    ↓
handle_403()
    ↓
check settings.DID_AUTH["ERROR_HANDLERS"]["403"]
    ↓
IF exists → use project function
ELSE → fallback to framework default
```

## How to use error handling in project
- example: `my_project/app_name/views.py`
```python

from django_did_auth.core.utils.errors import handle_error

return handle_error(request, 403, "You are not allowed to access this page.")
return handle_error(request, 429, "Too many attempts. Please try again later.")
return handle_error(request, 401, "Please login first.")

```

Examples:

- A) Role-based dashboard
```python
@login_required
def staff_dashboard_view(request):

    if request.user.role != "staff":
        return handle_error(request, 403, "Staff access only.")

    return render(request, "staff/dashboard.html")
```
- B) Profile ownership
```python
def profile_view(request, user_id):

    if request.user.id != user_id:
        return handle_error(request, 403, "You cannot view this profile.")

    ...
```
- C) API-style auth check
```python
def api_view(request):

    if not request.user.is_authenticated:
        return handle_error(request, 401, "Authentication required.")

    ...
```
- Object not found (manual 404)
```python
obj = MyModel.objects.filter(id=pk).first()

if not obj:
    return handle_error(request, 404, "Item not found.")
```


---

# Django RestFramework Settings

```python
INSTALLED_APPS += [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
]
# Please apply migrations for token_blacklist app to enable token blacklisting functionality
```

# Activate API Urls

- Include on your URL (`my_project/urls.py`)

```python
# Activate API routes
urlpatterns += [
    path("api/auth/", include("django_did_auth.api.urls")),
]
```


## Inside `django_did_auth.api.urls` (if you want use specific APIs):

```python
from django.urls import path
from .views import (
    ChangePasswordAPIView,
    APILoginView, 
    LogoutAPIView,
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView, 
    RegisterAPIView,
    ProfileAPIView, 
    TokenRefreshAPIView,
)

urlpatterns = [
    # JWT Token Refresh Endpoint
    path("refresh/", TokenRefreshAPIView.as_view(), name="api-refresh"),
    
    # Authentication Endpoints
    path("register/", RegisterAPIView.as_view(), name="api-register"),
    path("login/", APILoginView.as_view(), name="api-login"),
    path("logout/", LogoutAPIView.as_view(), name="api-logout"),
    
    # Password Reset Endpoints
    path("password-reset/", PasswordResetRequestAPIView.as_view(), name="api-password-reset-request"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmAPIView.as_view(), name="api-password-reset-confirm"),
    
    # User Profile & Password Change (Authenticated Endpoints)
    path("profile/", ProfileAPIView.as_view(), name="api-profile"),
    path("password-change/", ChangePasswordAPIView.as_view(), name="api-password-change"), 
    
]

 # Role-Based Access Control Endpoints Examples
 # from .views import HealthCheckAPIView, AdminOnlyAPIView, UserOnlyAPIView
"""
path("health/", HealthCheckAPIView.as_view(), name="api-health"),
path("admin-only/", AdminOnlyAPIView.as_view(), name="api-admin-only"),
path("user-only/", UserOnlyAPIView.as_view(), name="api-user-only"),
"""
```

## API security for your own API Views:

- is authenticated:

```python
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            ...

```

UI sample:

```html
<pre id="output"></pre>
<button id="getProfileBtn" type="button">Get Profile</button>
```
```javascript

    async function refreshToken() {
        const refresh = localStorage.getItem("refresh_token");

        const res = await fetch("http://127.0.0.1:8000/api/auth/refresh/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh })
        });

        const data = await res.json();

        if (data.access) {
            localStorage.setItem("access_token", data.access);
            localStorage.setItem("refresh_token", data.refresh);
            return true;
        }
        return false;
    }

    document.getElementById("getProfileBtn").addEventListener("click", async function() {
        let access = localStorage.getItem("access_token");

        let res = await fetch("http://127.0.0.1:8000/api/auth/profile/", {
            headers: { "Authorization": `Bearer ${access}` }
        });

        if (res.status === 401) {
            const ok = await refreshToken();
            if (!ok) {
                document.getElementById("output").textContent = "Session expired";
                return;
            }

            access = localStorage.getItem("access_token");

            res = await fetch("http://127.0.0.1:8000/api/auth/profile/", {
                headers: { "Authorization": `Bearer ${access}` }
            });
        }

        const data = await res.json();
        document.getElementById("output").textContent = JSON.stringify(data, null, 2);
    });
```

- admin access only:

```python
class AdminOnlyAPIView(APIView):
    permission_classes = [IsAuthenticated, role_access('admin')]

    def get(self, request):
        return Response({"message": "Admin access granted"})

# path("api/auth/admin-only/", AdminOnlyAPIView.as_view(), name="api-admin-only"),
```

```javascript
    document.getElementById("adminOnlyBtn").addEventListener("click", async function() {
        let access = localStorage.getItem("access_token");

        let res = await fetch("http://127.0.0.1:8000/api/auth/admin-only/", {
            headers: { "Authorization": `Bearer ${access}` }
        });

        if (res.status === 401) {
            const ok = await refreshToken();
            if (!ok) {
                document.getElementById("output").textContent = "Session expired";
                return;
            }

            access = localStorage.getItem("access_token");

            res = await fetch("http://127.0.0.1:8000/api/auth/admin-only/", {
                headers: { "Authorization": `Bearer ${access}` }
            });
        }

        const data = await res.json();
        document.getElementById("output").textContent = JSON.stringify(data, null, 2);
    });

```

- multiple role access:

```python
class UserOnlyAPIView(APIView):
    permission_classes = [IsAuthenticated, role_access('user')]

    def get(self, request):
        return Response({"message": "User access granted"})

# path("api/auth/user-only/", UserOnlyAPIView.as_view(), name="api-user-only"),
```
```javascript
    document.getElementById("userOnlyBtn").addEventListener("click", async function() {
        let access = localStorage.getItem("access_token");

        let res = await fetch("http://127.0.0.1:8000/api/auth/user-only/", {
            headers: { "Authorization": `Bearer ${access}` }
        });

        if (res.status === 401) {
            const ok = await refreshToken();
            if (!ok) {
                document.getElementById("output").textContent = "Session expired";
                return;
            }

            access = localStorage.getItem("access_token");

            res = await fetch("http://127.0.0.1:8000/api/auth/user-only/", {
                headers: { "Authorization": `Bearer ${access}` }
            });
        }

        const data = await res.json();
        document.getElementById("output").textContent = JSON.stringify(data, null, 2);
    });
```

- Sample Login / Logout:

```javascript
    document.getElementById("loginForm").addEventListener("submit", async function(e) {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("http://127.0.0.1:8000/api/auth/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            console.log(data);

            // Display response
            document.getElementById("output").textContent = JSON.stringify(data, null, 2);

            // Save token if success
            if (data.access) {
                localStorage.setItem("access_token", data.access);
                localStorage.setItem("refresh_token", data.refresh);
            }

        } catch (error) {
            document.getElementById("output").textContent = error;
        }
    });

    document.getElementById("logoutBtn").addEventListener("click", async function() {
        const accessToken = localStorage.getItem("access_token");
        const refreshToken = localStorage.getItem("refresh_token");

        if (!accessToken && !refreshToken) {
            document.getElementById("output").textContent = "No token found. Please login first.";
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/api/auth/logout/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });

            const data = await response.json();
            document.getElementById("output").textContent = JSON.stringify(data, null, 2);

            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
        } catch (error) {
            document.getElementById("output").textContent = error;
        }
    });
```

- Other existing URLs can be used:

```python
# Authentication Endpoints
http://127.0.0.1:8000/api/auth/register/
http://127.0.0.1:8000/api/auth/login/
http://127.0.0.1:8000/api/auth/logout/

# Password Reset Endpoints
http://127.0.0.1:8000/api/auth/password-reset/
http://127.0.0.1:8000/api/auth/password-reset-confirm/<uidb64>/<token>/

# User Profile & Password Change (Authenticated Endpoints)
http://127.0.0.1:8000/api/auth/profile/
http://127.0.0.1:8000/api/auth/password-change/
```


### Using throttle (ratelimiter for APIs):

- Public

```python
class PublicContentAPIView(APIView):
    throttle_classes = [
        PublicThrottle,
    ]

    def get(self, request):
        ...
```

- Public Readonly

```python
class PublicReadOnlyContentAPIView(APIView):
    throttle_classes = [
        PublicReadOnlyThrottle,
    ]

    def get(self, request):
        ...
```

- Authenticated

```python
class AuthenticatedAllRolesAPIView(APIView):
    throttle_classes = [
        AuthenticatedThrottle,
    ]

    def get(self, request):
        ...
```

- Post or Get Method aware

```python
class MethodAwarePublicContentAPIView(APIView):
    throttle_classes = [
        MethodAwarePublicThrottle,
    ]

    def get(self, request):
```

- APIKeyThrottle

```python
class RequiredAPIKeyContentView(APIView):
    throttle_classes = [
        APIKeyThrottle,
    ]

    def get(self, request):
```

---

# License
MIT License
# Author
Wilfred

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

# === default DID_AUTH config (can be overridden in dev/prod) ===
# https://pypi.org/project/django-did-auth/
DID_AUTH = {
    "LOGIN_REDIRECT": "/dashboard/",
    "LOGOUT_REDIRECT": "/login/",
    
    "ADMIN_URL": "admin/",
    "ADMIN_IP_WHITELIST": get_list_env("ADMIN_IP_WHITELIST", default=['127.0.0.1', '::1']),  # Localhost by default

    # on your URL
    # from django_did_auth.config.loader import get_admin_url
    # urlpatterns = [
    #     path(get_admin_url(), admin.site.urls),
    # ]

    "ROLES": {
        "admin": "/admin-dashboard/",
        "staff": "/staff-dashboard/",
        "moderator": "/moderator-dashboard/",
        "user": "/dashboard/",
    },

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
    'rest_framework',
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
DID_AUTH = {
    "LOGIN_REDIRECT": "/dashboard/",
    "LOGOUT_REDIRECT": "/auth/login/",
    "ADMIN_URL": "secret-admin/",
    "ADMIN_IP_WHITELIST": get_list_env("ADMIN_IP_WHITELIST", default=['127.0.0.1', '::1']),
    "ROLES": {
        "owner": "/dashboard/owner/",
        "manager": "/dashboard/manager/",
        "staff": "/dashboard/staff/",
    },
}
# Admin security
MIDDLEWARE.insert(0, 'django_did_auth.security.admin.ipwhitelist.AdminIPWhitelistMiddleware')
```

## Environment Variables (.env)
```env
# dev | prod | local
DJANGO_ENV=dev                    
SECRET_KEY='your-secret-key'
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://yourdomain.com
REDIS_URL=redis://127.0.0.1:6379/1

EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password

ADMIN_IP_WHITELIST=127.0.0.1,192.168.68.100
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
- `AUTH_USER_MODEL`
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

### For authentication
- to customized authentication (settings & UI), please visit `https://pypi.org/project/django-did-auth/`

# License
MIT License
# Author
Wilfred


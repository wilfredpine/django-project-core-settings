# django-project-core-settings - Configuration Guide

Production-ready modular Django settings with strong security defaults.

## Features Summary

- Environment-based configuration (`dev` / `prod` / `local`)
- Strong security hardening by default
- Plug-and-play extensibility
- Structured logging with JSON support
- SAUTH integration ready

## Recommended Usage Pattern

```python
# myproject/settings.py
from django_project_core_settings import *

from django_project_core_settings.utils.env import get_list_env

# === Extend with your apps ===
INSTALLED_APPS += [
    'users',
    # 'blog',
    # 'portfolio',
    # 'ckeditor',
]

MIDDLEWARE += [
    # 'your.middleware.Class',
]

# === Common overrides ===
LOGIN_REDIRECT_URL = '/dashboard/'
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# === Security & Domain ===
ALLOWED_HOSTS = get_list_env("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])

# Add frontend domains if needed
CSRF_TRUSTED_ORIGINS += [
    "https://your-frontend.com",
]

# === default SAUTH config (can be overridden in dev/prod) ===
SAUTH = {
    "LOGIN_REDIRECT": "/dashboard/",
    "LOGOUT_REDIRECT": "/auth/login/",
    "ROLES": {
        "admin": "/dashboard/admin/",
        "staff": "/dashboard/staff/",
        "moderator": "/dashboard/moderator/",
        "user": "/dashboard/",
    },
    "UI_FRAMEWORK": "tailwind",
    "RATE_LIMIT": {
        "LOGIN": "10/m",
        "REGISTER": "5/m",
    },
}
# =============================================
# === SAUTH Customization ===
SAUTH['ROLES'].update({
    'editor': '/dashboard/editor/',
    'author': '/dashboard/author/',
})

# Obscure admin URL
ADMIN_URL = 'hidden-admin-xyz123/'
# on your URL
# urlpatterns = [
#     path(settings.ADMIN_URL, admin.site.urls),
# ]

# Additinal settings can be added here as needed
# E.g.
# Admin security
ADMIN_IP_WHITELIST = get_list_env("ADMIN_IP_WHITELIST", default=[])
mw = 'core.middleware.admin_security.AdminIPWhitelistMiddleware'
if mw not in MIDDLEWARE:
    MIDDLEWARE.append(mw)
# Create these middleware and logic to restrict access to admin based on IP whitelist
# myproject/core/middleware/admin_security.py
'''
# core/middleware/admin_security.py
from django.conf import settings
from django.http import HttpResponseForbidden
from django_sauth.security.audit.logger import get_client_ip, audit_logger
class AdminIPWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_path = f"/{settings.ADMIN_URL.strip('/')}/"
    def __call__(self, request):
        # ✅ Skip in development
        # if settings.DEBUG:
        #     return self.get_response(request)
        path = request.path.rstrip("/") + "/"
        if path.startswith(self.admin_path):
            allowed_ips = [ip.strip() for ip in settings.ADMIN_IP_WHITELIST if ip.strip()]
            if allowed_ips:
                client_ip = get_client_ip(request)
                if client_ip not in allowed_ips:
                    audit_logger.warning(
                        "admin_access_blocked",
                        extra={"ip": client_ip, "path": request.path}
                    )
                    return HttpResponseForbidden("Forbidden")
        return self.get_response(request)'''

```

## Environment Variables
See `.env.example` or use the following:
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

## What Should NOT Be Overridden
- `SECRET_KEY`
- `DEBUG` (controlled by `DJANGO_ENV`)
- `AUTH_USER_MODEL`
- `AUTHENTICATION_BACKENDS`
- Core `MIDDLEWARE` order (use `MIDDLEWARE += []` )
- Security settings like `SECURE_HSTS_SECONDS`, `SESSION_COOKIE_SECURE`, etc.

## Testing Settings
```bash
DJANGO_ENV=dev  python manage.py check
DJANGO_ENV=prod python manage.py check
```
## Logging Locations

- `logs/app.log`
- `logs/security.log` (important for login attempts, lockouts)
- `logs/error.log`


## Project Structure

```bash
django_project_core_settings/
├── base.py
├── dev.py
├── prod.py
├── local.py
├── components/
│   ├── apps.py
│   ├── auth.py
│   ├── security.py
│   ├── logging.py
│   └── ...
└── utils/
    └── env.py
```

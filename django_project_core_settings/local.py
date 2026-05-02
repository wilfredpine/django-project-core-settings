
from .base import *
from .utils.env import get_list_env

DEBUG = False
DID_AUTH = DID_AUTH_CONFIG(DEBUG)

ALLOWED_HOSTS = get_list_env("ALLOWED_HOSTS", required=True)

CSRF_TRUSTED_ORIGINS = get_list_env("CSRF_TRUSTED_ORIGINS")
if not CSRF_TRUSTED_ORIGINS:
    raise ValueError("! CSRF_TRUSTED_ORIGINS is highly recommended in production")

# Strict security bypass for local 
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# CSP stricter in production
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'",)
CSP_REPORT_ONLY = False

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATA_UPLOAD_MAX_MEMORY_SIZE = 2 * 1024 * 1024  # 2MB

# Internal IPs for debug toolbar
INTERNAL_IPS = ALLOWED_HOSTS # ['127.0.0.1']

INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
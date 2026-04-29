# settings/dev.py
from .base import *
from .utils.env import get_bool_env, get_list_env

DEBUG = get_bool_env("DEBUG", True)

ALLOWED_HOSTS = get_list_env("ALLOWED_HOSTS", ["localhost", "127.0.0.1", "0.0.0.0"])
CSRF_TRUSTED_ORIGINS = get_list_env(
    "CSRF_TRUSTED_ORIGINS", 
    ["http://localhost:8000", "http://127.0.0.1:8000"]
)

# Relax security for development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# SAUTH
SAUTH = SAUTH_CONFIG(DEBUG)
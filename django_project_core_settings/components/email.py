# settings/components/email.py
from ..utils.env import get_env, get_bool_env

EMAIL_HOST = get_env("EMAIL_HOST")
EMAIL_PORT = int(get_env("EMAIL_PORT", 587))
EMAIL_USE_TLS = get_bool_env("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = get_env("EMAIL_USER")
EMAIL_HOST_PASSWORD = get_env("EMAIL_PASS")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Default (will be overridden in dev/prod)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
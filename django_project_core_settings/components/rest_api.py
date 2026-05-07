
# ----------------------------------------------------------------------------------
# REST FRAMEWORK & JWT for API authentication
# ----------------------------------------------------------------------------------
from datetime import timedelta
from django_project_core_settings.utils.env import get_list_env, get_env
from django_did_auth.security.ratelimit.decorators import is_redis_available

# if get_env("ENABLE_REST_API", default="false").lower() == "true":

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",  # or RS256 (advanced)
    "SIGNING_KEY": get_env("JWT_SIGNING_KEY"), # Rotate this key periodically for security
}

if is_redis_available():
    REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = [
        'django_did_auth.security.ratelimit.api_throttles.PublicReadOnlyThrottle',
        'django_did_auth.security.ratelimit.api_throttles.MethodAwarePublicThrottle',
        'django_did_auth.security.ratelimit.api_throttles.APIKeyThrottle',
        'django_did_auth.security.ratelimit.api_throttles.PublicThrottle',
        'django_did_auth.security.ratelimit.api_throttles.AuthenticatedThrottle',
    ]
else:
    REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
    SILENCED_SYSTEM_CHECKS = [
        "django_ratelimit.E003",
        "django_ratelimit.W001",
    ]
    
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    
    "api_public_readonly": get_env("API_PUBLIC_READONLY_RATE", default="200/min"),
    
    "public_get": get_env("PUBLIC_GET_RATE", default="200/min"),
    "public_post": get_env("PUBLIC_POST_RATE", default="50/min"),
    
    "api_key": get_env("API_KEY_RATE", default="200/min"),
    
    "api_public": get_env("API_PUBLIC_RATE", default="100/day"),
    "api_authenticated": get_env("API_AUTHENTICATED_RATE", default="1000/day"),

    "login_ip": get_env("LOGIN_IP_RATE", default="10/min"),
    "login_email": get_env("LOGIN_EMAIL_RATE", default="5/min"),

    "register_ip": get_env("REGISTER_IP_RATE", default="5/min"),
    "register_email": get_env("REGISTER_EMAIL_RATE", default="3/min"),

    "password_reset_request": get_env("PASSWORD_RESET_REQUEST_RATE", default="3/min"),
    "password_reset_confirm": get_env("PASSWORD_RESET_CONFIRM_RATE", default="10/min"),

    "change_password": get_env("CHANGE_PASSWORD_RATE", default="5/min"),
}
REST_FRAMEWORK["EXCEPTION_HANDLER"] = "django_did_auth.api.views.custom_exception_handler"
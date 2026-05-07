# settings/components/cache.py

from ..utils.env import get_env

DJANGO_ENV = get_env("DJANGO_ENV", "prod").lower()
REDIS_REQUIRED = get_env("REDIS_REQUIRED", "false").lower() == "true"
REDIS_URL = get_env("REDIS_URL", "redis://127.0.0.1:6379/1")


# --------------------------------------------------
# AXES CONFIG (independent of Redis availability)
# --------------------------------------------------
AXES_ENABLED = True

# Axes fallback behavior
# False = Fail Closed (secure) | app becomes unusable if Redis is down → recommended for maximum security in production
# True = Fail Open (usable) | app continues but reduced security (no rate limiting, no lockouts) → use only if you have a reliable Redis connection in production
if DJANGO_ENV == "prod":
    AXES_FAIL_SILENTLY = False  # fail closed (secure)
else:
    AXES_FAIL_SILENTLY = True   # dev/local flexibility


# --------------------------------------------------
# CACHE CONFIG
# --------------------------------------------------
if REDIS_REQUIRED:
    if DJANGO_ENV == "prod" and not REDIS_URL:
        raise ValueError("REDIS_URL required in production")

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "TIMEOUT": 300,
        }
    }

else:
    # fallback (DEV / NO REDIS)
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "dev-cache",
        }
    }


# --------------------------------------------------
# OPTIONAL: Runtime Redis Health Check (ONLY PROD)
# --------------------------------------------------
if REDIS_REQUIRED and DJANGO_ENV == "prod":
    try:
        from django_redis import get_redis_connection
        conn = get_redis_connection("default")
        conn.ping()
    except Exception as e:
        raise Exception(f" Redis not reachable: {e}")
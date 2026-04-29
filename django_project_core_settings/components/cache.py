# settings/components/cache.py
from ..utils.env import get_env

REDIS_URL = get_env("REDIS_URL", "redis://127.0.0.1:6379/1")

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    }
}
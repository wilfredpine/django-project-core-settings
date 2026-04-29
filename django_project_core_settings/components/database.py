# settings/components/database.py
from ..utils.paths import BASE_DIR
from ..utils.path_validator import to_str
from ..utils.env import get_env

DATABASES = {
    'default': {
        'ENGINE': get_env('DB_ENGINE', 'django.db.backends.sqlite3'),
        "NAME": to_str(
            BASE_DIR / get_env("DB_NAME", "db.sqlite3")
        ),
        'USER': get_env('DB_USER', ''),
        'PASSWORD': get_env('DB_PASSWORD', ''),
        'HOST': get_env('DB_HOST', ''),
        'PORT': get_env('DB_PORT', ''),
    }
}
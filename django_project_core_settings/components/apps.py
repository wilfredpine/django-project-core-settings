# settings/components/apps.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Security & utilities
    'axes',
    'django_ratelimit',
    'django_did_auth',          # if you're using it

    # Your core apps
    # 'users',
    # 'apps.main',
]

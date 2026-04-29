from .dev import *

INTERNAL_IPS = ['127.0.0.1']

EXTRA_INSTALLED_APPS += ['debug_toolbar']
EXTRA_MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Optional: override DB for local development
# DATABASES['default']['NAME'] = BASE_DIR / 'local_db.sqlite3'
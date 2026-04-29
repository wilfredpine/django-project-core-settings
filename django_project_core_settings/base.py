# settings/base.py
from .utils.paths import BASE_DIR

from .utils.path_validator import ensure_dirs

# 📁 Ensure core directories exist
ensure_dirs(
    BASE_DIR / "logs",
    BASE_DIR / "media",
    BASE_DIR / "staticfiles",
)

# =============================================
# CORE SETTINGS
# =============================================
from .components.core import *
from .components.apps import *
from .components.middleware import *
from .components.auth import *
from .components.sauth import *
from .components.database import *
from .components.cache import *
from .components.rate_limit import *
from .components.security import *
from .components.csp import *
from .components.static import *
from .components.email import *
from .components.logging import *

# =============================================
# TEMPLATES
# =============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = "project_core.urls"
WSGI_APPLICATION = "project_core.wsgi.application"
SITE_ID = 1


from ..utils.paths import BASE_DIR
from ..utils.path_validator import ensure_dir
 
STATIC_URL = "/static/"
STATIC_ROOT = ensure_dir(BASE_DIR / "staticfiles")

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = ensure_dir(BASE_DIR / "media")

# WhiteNoise configuration will be adjusted in dev/prod if needed
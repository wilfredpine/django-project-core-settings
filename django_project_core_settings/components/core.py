# settings/components/core.py
from ..utils.env import get_env

SECRET_KEY = get_env("SECRET_KEY", required=True)

TIME_ZONE = get_env("TIME_ZONE", "UTC")
USE_TZ = True
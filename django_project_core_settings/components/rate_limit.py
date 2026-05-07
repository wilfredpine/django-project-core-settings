from django_project_core_settings.utils.env import get_env

RATELIMIT_USE_CACHE = 'default'
RATELIMIT_VIEW = 'ratelimit.views.RatelimitView'

# --------------------------------------------------
# AXES HARDENING (ALIGNED)
# --------------------------------------------------
AXES_VERBOSE = True # (optional) Log lockouts with more detail (check logs → you’ll see exactly why login fails)
AXES_CACHE = 'default'
AXES_FAILURE_LIMIT = int(get_env("AXES_FAILURE_LIMIT", default=5))
AXES_COOLOFF_TIME = int(get_env("AXES_COOLOFF_TIME", default=30))
AXES_RESET_ON_SUCCESS = True
AXES_USERNAME_FORM_FIELD = 'email'
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']
# Optional UI override
AXES_LOCKOUT_TEMPLATE = 'did_auth/lockout.html'
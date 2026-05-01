# settings/components/logging.py
from ..utils.paths import BASE_DIR
from ..utils.path_validator import ensure_dir

# Ensure logs directory exists
LOG_DIR = ensure_dir(BASE_DIR / "logs")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s %(name)s %(pathname)s:%(lineno)d: %(message)s",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(event)s %(ip)s %(user_id)s %(email)s %(path)s %(status_code)s",
            "rename_fields": {"asctime": "timestamp", "levelname": "level"},
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        },
        "app_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "app.log",
            "when": "midnight",
            "backupCount": 14,
            "encoding": "utf-8",
            "formatter": "verbose",
        },
        "security_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "security.log",
            "when": "midnight",
            "backupCount": 30,
            "encoding": "utf-8",
            "formatter": "json",
        },
        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "error.log",
            "when": "midnight",
            "backupCount": 30,
            "encoding": "utf-8",
            "formatter": "json",
            "level": "ERROR",
        },
    },

    "loggers": {
        # Django core
        "django": {
            "handlers": ["app_file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console", "app_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },

        # Application logs
        "app": {
            "handlers": ["console", "app_file"],
            "level": "INFO",
            "propagate": False,
        },

        # Security & Audit
        "security": {
            "handlers": ["console", "security_file"],
            "level": "INFO",
            "propagate": False,
        },
        "did_auth.audit": {
            "handlers": ["console", "security_file"],
            "level": "INFO",
            "propagate": False,
        },
        "axes": {
            "handlers": ["console", "security_file"],
            "level": "WARNING",
            "propagate": False,
        },
        "ratelimit": {
            "handlers": ["console", "security_file"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
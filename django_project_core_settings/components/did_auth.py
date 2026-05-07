from django_project_core_settings.utils.env import get_env

def get_did_auth_config(debug: bool):
    return {
        "LOGIN_REDIRECT": "/dashboard/",
        "LOGOUT_REDIRECT": "/auth/login/",
        "ADMIN_URL": "admin/",
        "ADMIN_IP_WHITELIST": get_env("ADMIN_IP_WHITELIST", default=['127.0.0.1', '::1']),  # Localhost by default

        "ROLES": {
            """Override these with your actual role names and redirect URLs""",
            # "admin": "/admin-dashboard/",
            # "user": "/dashboard/",
        },
        
        "DENY_BEHAVIOR": "forbidden",  # or "redirect"

        "EMAIL": {
            "VERIFY_EXPIRY_HOURS": 24,
            "RESET_EXPIRY_HOURS": 1,
            "FROM_EMAIL": None,  # Will use DEFAULT_FROM_EMAIL
        },

        "RATE_LIMIT": {
            "LOGIN": get_env("LOGIN_RATE", default="10/m"),
            "REGISTER": get_env("REGISTER_RATE", default="5/m"),
            "PASSWORD_RESET": get_env("PASSWORD_RESET_RATE", default="5/m"),
        },

        "UI_FRAMEWORK": "tailwind",  # "tailwind" or "bootstrap"

        "ENABLE_AUDIT": True,
        "TRUST_PROXY": not debug,
        
        "SECURITY": {
            "PASSWORD_MIN_LENGTH": 12,
            "ENABLE_AXES": True,
            "LOCKOUT_AFTER_ATTEMPTS": 5,
            "LOCKOUT_DURATION_MINUTES": 30,
            "REQUIRE_HTTPS": True,          # Enforce in production
        },
        "AUDIT": {
            "ENABLED": True,
            "LOG_SENSITIVE": False,         # Don't log passwords
        }
        
    }


DID_AUTH_CONFIG = get_did_auth_config  # expose the function
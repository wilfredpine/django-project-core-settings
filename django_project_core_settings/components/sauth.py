
def get_sauth_config(debug: bool):
    return {
        "LOGIN_REDIRECT": "/dashboard/",
        "LOGOUT_REDIRECT": "/auth/login/",
        "ROLES": {
            "admin": "/dashboard/admin/",
            "staff": "/dashboard/staff/",
            "moderator": "/dashboard/moderator/",
            "user": "/dashboard/",
        },
        "UI_FRAMEWORK": "tailwind",
        "RATE_LIMIT": {
            "LOGIN": "10/m",
            "REGISTER": "5/m",
        },
        "TRUST_PROXY": not debug,
    }


SAUTH_CONFIG = get_sauth_config  # expose the function
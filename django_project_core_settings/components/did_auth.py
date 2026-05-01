
def get_did_auth_config(debug: bool):
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


DID_AUTH_CONFIG = get_did_auth_config  # expose the function
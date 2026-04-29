AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = 'sauth:login'
LOGIN_REDIRECT_URL = '/dashboard/'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
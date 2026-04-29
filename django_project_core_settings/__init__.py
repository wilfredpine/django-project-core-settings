import os
from .utils.env import init_env

init_env()

env = os.getenv("DJANGO_ENV", "dev").lower()

if env == "prod":
    from .prod import *
elif env == "local":
    from .local import *
else:
    from .dev import *
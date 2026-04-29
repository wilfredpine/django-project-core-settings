# django_project_core_settings/utils/paths.py

import os
from pathlib import Path

def get_base_dir() -> Path:
    """Return project root directory (safe for pip + local)."""
    return Path(os.getenv("BASE_DIR", Path.cwd())).resolve()


# 🔥 SINGLE SOURCE OF TRUTH
BASE_DIR = get_base_dir()
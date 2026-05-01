# settings/utils/env.py
import os
from typing import Any
from dotenv import load_dotenv
from pathlib import Path

def init_env():
    """Load .env from project root (portable)."""
    current = Path.cwd()

    for parent in [current] + list(current.parents):
        env_path = parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            return

    load_dotenv()  # fallback

def get_env(key: str, default: Any = None, required: bool = False) -> Any:
    """Get environment variable."""
    value = os.getenv(key, default)
    if required and not value and value != 0:
        raise ValueError(f"{key} is required but not set in .env")
    return value


def get_bool_env(key: str, default: bool = False) -> bool:
    """Return boolean from environment variable."""
    value = os.getenv(key, str(default)).lower().strip()
    return value in ('true', '1', 'yes', 'on', 'y')


def get_list_env(key: str, default: list | None = None, separator: str = ",", required: bool = False) -> list[str]:
    """Convert comma-separated string to list. Supports required."""
    value = os.getenv(key)
    if required and not value:
        raise ValueError(f"{key} is required but not set in .env")
    if not value:
        return default or []
    return [x.strip() for x in value.split(separator) if x.strip()]


def get_path_env(key: str, default: str | Path | None = None) -> Path:
    """Get path from environment variable."""
    value = os.getenv(key)
    if value:
        return Path(value)
    return Path(default) if default else Path.cwd()
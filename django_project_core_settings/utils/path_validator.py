# django_project_core_settings/utils/path_validator.py

from pathlib import Path


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_dirs(*paths: Path) -> None:
    """Ensure multiple directories exist."""
    for path in paths:
        ensure_dir(path)


def validate_path(path: Path, must_exist: bool = False, name: str = "Path") -> Path:
    """Validate a path safely."""
    if must_exist and not path.exists():
        raise ValueError(f"❌ {name} does not exist: {path}")
    return path


def to_str(path: Path) -> str:
    """Convert Path to string safely (for DB compatibility)."""
    return str(path)
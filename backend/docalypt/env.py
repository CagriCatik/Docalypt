"""Helpers for loading .env files into the process environment."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENV_FILENAMES = (".env",)

_ENV_LOADED = False


def load_env(paths: Iterable[Path] | None = None) -> None:
    """Load environment variables from .env files if present."""

    global _ENV_LOADED
    if _ENV_LOADED:
        return

    candidates: list[Path] = []
    if paths is not None:
        candidates.extend(Path(p).expanduser() for p in paths)
    else:
        cwd = Path.cwd()
        for name in DEFAULT_ENV_FILENAMES:
            candidates.append(cwd / name)
            candidates.append(PROJECT_ROOT / name)

    for path in candidates:
        if path.exists() and path.is_file():
            _apply_env_file(path)
            break

    _ENV_LOADED = True


def _apply_env_file(path: Path) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip()
        if value and ((value[0] == value[-1]) and value[0] in {'"', "'"}):
            value = value[1:-1]
        os.environ.setdefault(key, value)


__all__ = ["load_env", "PROJECT_ROOT"]


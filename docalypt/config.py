"""Compatibility wrapper for configuration helpers."""

from __future__ import annotations

from docalypt.infrastructure.config.toml_loader import (  # noqa: F401
    AppConfig,
    CONFIG_DIR,
    CONFIG_PATH,
    load_app_config as load_config,
)

__all__ = ["AppConfig", "load_config", "CONFIG_PATH", "CONFIG_DIR"]

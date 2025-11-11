"""Configuration handling for Docalypt."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import toml

CONFIG_DIR = Path.home() / ".config" / "docalypt"
CONFIG_PATH = CONFIG_DIR / "config.toml"


@dataclass(slots=True)
class AppConfig:
    """Runtime configuration values."""

    marker_regex: str = r"\((\d{1,2}:\d{2}(?::\d{2})?)\)"
    output_dir: Path = Path.home() / "chapters"
    html_template: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "marker_regex": self.marker_regex,
            "output_dir": str(self.output_dir),
            "html_template": self.html_template,
        }


def load_config() -> AppConfig:
    """Load configuration from disk, falling back to defaults."""

    if not CONFIG_PATH.exists():
        return AppConfig()

    try:
        data = toml.load(CONFIG_PATH)
    except Exception:
        return AppConfig()

    config = AppConfig()
    if "marker_regex" in data:
        config.marker_regex = str(data["marker_regex"])
    if "output_dir" in data:
        config.output_dir = Path(data["output_dir"]).expanduser().resolve()
    if "html_template" in data:
        raw = data["html_template"]
        config.html_template = str(raw) if raw is not None else None
    return config


__all__ = ["AppConfig", "load_config", "CONFIG_PATH", "CONFIG_DIR"]

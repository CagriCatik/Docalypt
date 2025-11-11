"""Infrastructure helpers for loading application configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import toml

CONFIG_DIR = Path.home() / ".config" / "docalypt"
CONFIG_PATH = CONFIG_DIR / "config.toml"


@dataclass(slots=True)
class AppConfig:
    marker_regex: str = r"\((\d{1,2}:\d{2}(?::\d{2})?)\)"
    output_dir: Path = Path.home() / "chapters"
    html_template: Path | None = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "marker_regex": self.marker_regex,
            "output_dir": str(self.output_dir),
            "html_template": str(self.html_template) if self.html_template else None,
        }


def load_app_config() -> AppConfig:
    if not CONFIG_PATH.exists():
        return AppConfig()

    try:
        raw = toml.load(CONFIG_PATH)
    except Exception:
        return AppConfig()

    config = AppConfig()
    if marker := raw.get("marker_regex"):
        config.marker_regex = str(marker)
    if output := raw.get("output_dir"):
        config.output_dir = Path(output).expanduser().resolve()
    if template := raw.get("html_template"):
        path = Path(template).expanduser().resolve()
        config.html_template = path if path.exists() else None
    return config


__all__ = ["AppConfig", "CONFIG_DIR", "CONFIG_PATH", "load_app_config"]

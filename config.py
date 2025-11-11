# File: config.py
from pathlib import Path
import toml

# Default application configuration
DEFAULT_CONFIG = {
    "marker_regex": r"\((\d{1,2}:\d{2}(?::\d{2})?)\)",
    "output_dir": str(Path.home() / "chapters"),
    "html_template": None,
}


def load_config() -> dict:
    """
    Load user config from ~/.config/markdown_splitter/config.toml.
    Falls back to DEFAULT_CONFIG if not present.
    """
    config_dir = Path.home() / ".config" / "markdown_splitter"
    config_path = config_dir / "config.toml"
    if config_path.exists():
        try:
            return toml.load(config_path)
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


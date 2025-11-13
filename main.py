"""Entry point for the full Docalypt GUI."""

from __future__ import annotations

from docalypt.env import load_env
from docalypt.gui.main_window import run


if __name__ == "__main__":
    load_env()
    run()

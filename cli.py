"""Command-line interface for Docalypt."""

from __future__ import annotations

from docalypt.interfaces.cli.app import app


def cli() -> None:  # pragma: no cover - thin wrapper for entry points
    app()


if __name__ == "__main__":  # pragma: no cover - CLI execution
    cli()

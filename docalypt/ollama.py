"""Compatibility wrappers around the infrastructure Ollama gateway."""

from __future__ import annotations

from docalypt.infrastructure.llm import ollama as _ollama
from docalypt.infrastructure.llm.ollama import *  # noqa: F401,F403

__all__ = _ollama.__all__  # type: ignore[attr-defined]

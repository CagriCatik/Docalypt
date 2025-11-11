"""Docalypt application package."""

from .config import AppConfig, load_config
from .splitting import TranscriptSplitter
from .documentation import (
    OllamaSettings,
    DocumentGenerationRequest,
    DocumentGenerationResult,
    collect_chapter_files,
    generate_documentation,
)

__all__ = [
    "AppConfig",
    "DocumentGenerationRequest",
    "DocumentGenerationResult",
    "OllamaSettings",
    "TranscriptSplitter",
    "collect_chapter_files",
    "generate_documentation",
    "load_config",
]

"""Docalypt application package."""

from .config import AppConfig, load_config
from .splitting import TranscriptSplitter
from .documentation import (
    DOCUMENTATION_SUBDIR,
    OllamaSettings,
    DocumentGenerationRequest,
    DocumentGenerationResult,
    collect_chapter_files,
    generate_documentation,
)

__all__ = [
    "AppConfig",
    "DOCUMENTATION_SUBDIR",
    "DocumentGenerationRequest",
    "DocumentGenerationResult",
    "OllamaSettings",
    "TranscriptSplitter",
    "collect_chapter_files",
    "generate_documentation",
    "load_config",
]

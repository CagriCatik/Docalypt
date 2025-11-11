"""Docalypt application package."""

from docalypt.application.generate_docs import GenerateDocumentationUseCase
from docalypt.application.split_transcript import SplitTranscriptUseCase
from docalypt.config import AppConfig, load_config
from docalypt.documentation import (
    DOCUMENTATION_SUBDIR,
    DocumentOutcome,
    OllamaError,
    OllamaSettings,
    collect_chapter_files,
    generate_documentation,
)
from docalypt.infrastructure.llm.ollama import PROMPT_TEMPLATE, build_prompt
from docalypt.infrastructure.storage.filesystem import FileSystemChapterRepository
from docalypt.splitting import SplitResult, TranscriptSplitter

__all__ = [
    "AppConfig",
    "DOCUMENTATION_SUBDIR",
    "DocumentOutcome",
    "FileSystemChapterRepository",
    "GenerateDocumentationUseCase",
    "OllamaError",
    "OllamaSettings",
    "PROMPT_TEMPLATE",
    "SplitResult",
    "SplitTranscriptUseCase",
    "TranscriptSplitter",
    "build_prompt",
    "collect_chapter_files",
    "generate_documentation",
    "load_config",
]

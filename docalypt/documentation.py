"""Compatibility layer exposing documentation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from docalypt.application.generate_docs import GenerateDocumentationUseCase
from docalypt.domain.models import DocumentOutcome
from docalypt.infrastructure.llm.ollama import (
    OllamaError,
    OllamaGateway,
    OllamaSettings,
    PROMPT_TEMPLATE,
    build_prompt,
)

DOCUMENTATION_SUBDIR = "documentation"


def collect_chapter_files(output_dir: Path) -> list[Path]:
    """Return a sorted list of chapter files ready for documentation."""

    files = [
        path
        for path in sorted(output_dir.glob("*.md"))
        if not path.name.endswith(".docs.md")
    ]
    return files


def generate_documentation(
    chapters: Sequence[Path],
    settings: OllamaSettings,
    destination_dirname: str = DOCUMENTATION_SUBDIR,
    prompt_template: str | None = None,
) -> DocumentOutcome:
    """Generate documentation for provided chapters using Ollama."""

    gateway = OllamaGateway(settings=settings)
    use_case = GenerateDocumentationUseCase(gateway=gateway)
    return use_case.execute(
        chapters=chapters,
        destination_dirname=destination_dirname,
        prompt_template=prompt_template,
    )


__all__ = [
    "DOCUMENTATION_SUBDIR",
    "DocumentOutcome",
    "OllamaError",
    "OllamaSettings",
    "PROMPT_TEMPLATE",
    "build_prompt",
    "collect_chapter_files",
    "generate_documentation",
]

"""High-level documentation generation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .llm import (
    LLMError,
    LLMSettings,
    PROMPT_TEMPLATE,
    build_prompt,
    create_client,
    OllamaSettings,
)


DOCUMENTATION_SUBDIR = "documentation"


@dataclass(slots=True)
class DocumentGenerationRequest:
    chapters: Sequence[Path]
    settings: LLMSettings
    prompt_template: str | None = None
    destination_dirname: str = DOCUMENTATION_SUBDIR


@dataclass(slots=True)
class DocumentGenerationResult:
    written: list[tuple[Path, Path]]  # (chapter, documentation)
    failures: list[tuple[Path, str]]

    @property
    def success(self) -> bool:
        return not self.failures


def collect_chapter_files(output_dir: Path) -> list[Path]:
    """Return a sorted list of chapter files ready for documentation."""

    files = [
        path
        for path in sorted(output_dir.glob("*.md"))
        if not path.name.endswith(".docs.md")
    ]
    return files


def generate_documentation(request: DocumentGenerationRequest) -> DocumentGenerationResult:
    """Generate documentation for provided chapters using the configured LLM."""

    client = create_client(request.settings)
    written: list[tuple[Path, Path]] = []
    failures: list[tuple[Path, str]] = []

    created_dirs: set[Path] = set()
    for chapter in request.chapters:
        try:
            chapter_text = chapter.read_text(encoding="utf-8")
            template = request.prompt_template or PROMPT_TEMPLATE
            prompt = build_prompt(chapter.name, chapter_text, template)
            markdown = client.generate(prompt)
            destination_dir = chapter.parent / request.destination_dirname
            if destination_dir not in created_dirs:
                destination_dir.mkdir(parents=True, exist_ok=True)
                created_dirs.add(destination_dir)
            destination = destination_dir / f"{chapter.stem}.docs.md"
            destination.write_text(markdown, encoding="utf-8")
            written.append((chapter, destination))
        except LLMError as exc:
            failures.append((chapter, str(exc)))
        except Exception as exc:  # pragma: no cover - safety net
            failures.append((chapter, str(exc)))
    return DocumentGenerationResult(written=written, failures=failures)


__all__ = [
    "DOCUMENTATION_SUBDIR",
    "DocumentGenerationRequest",
    "DocumentGenerationResult",
    "LLMSettings",
    "OllamaSettings",
    "collect_chapter_files",
    "generate_documentation",
]

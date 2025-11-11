"""High-level documentation generation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from .ollama import OllamaClient, OllamaError, OllamaSettings, build_prompt


@dataclass(slots=True)
class DocumentGenerationRequest:
    chapters: Sequence[Path]
    settings: OllamaSettings


@dataclass(slots=True)
class DocumentGenerationResult:
    written: list[Path]
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
    """Generate documentation for provided chapters using Ollama."""

    client = OllamaClient(settings=request.settings)
    written: list[Path] = []
    failures: list[tuple[Path, str]] = []

    for chapter in request.chapters:
        try:
            chapter_text = chapter.read_text(encoding="utf-8")
            prompt = build_prompt(chapter.name, chapter_text)
            markdown = client.generate(prompt)
            destination = chapter.with_name(f"{chapter.stem}.docs.md")
            destination.write_text(markdown, encoding="utf-8")
            written.append(destination)
        except OllamaError as exc:
            failures.append((chapter, str(exc)))
        except Exception as exc:  # pragma: no cover - safety net
            failures.append((chapter, str(exc)))
    return DocumentGenerationResult(written=written, failures=failures)


__all__ = [
    "DocumentGenerationRequest",
    "DocumentGenerationResult",
    "OllamaSettings",
    "collect_chapter_files",
    "generate_documentation",
]

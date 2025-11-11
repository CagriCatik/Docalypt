"""Application layer protocols and shared types."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Protocol, Sequence

from docalypt.domain.models import ChapterDocument, DocumentOutcome, SplitTranscript


class ProgressReporter(Protocol):
    """Protocol for objects reporting progress events."""

    def __call__(self, current: int, total: int) -> None:  # pragma: no cover - typing only
        ...


class ChapterRepository(Protocol):
    """Persistence boundary for storing chapter documents."""

    def save_documents(
        self,
        documents: Sequence[ChapterDocument],
        export_html: bool,
    ) -> tuple[list[Path], Path | None]:
        ...

    def render_html_index(self, documents: Sequence[ChapterDocument]) -> Path:
        ...


class DocumentationGateway(Protocol):
    """Boundary for generating chapter documentation."""

    def generate_documents(
        self,
        job_chapters: Sequence[Path],
        destination_dirname: str,
        prompt_template: str | None,
    ) -> DocumentOutcome:
        ...


__all__ = [
    "ProgressReporter",
    "ChapterRepository",
    "DocumentationGateway",
]

"""Domain models for transcripts and generated documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True, slots=True)
class Chapter:
    """Represents a chapter marker discovered in a transcript."""

    index: int
    title: str
    timestamp: int


@dataclass(frozen=True, slots=True)
class ChapterDocument:
    """Markdown output for a chapter."""

    chapter: Chapter
    content: str


@dataclass(slots=True)
class SplitTranscript:
    """Result of splitting a transcript into chapter documents."""

    documents: list[ChapterDocument]

    def __iter__(self):  # pragma: no cover - convenience for callers
        yield from self.documents

    def __len__(self) -> int:  # pragma: no cover - convenience for callers
        return len(self.documents)


@dataclass(slots=True)
class DocumentJob:
    """Request payload for documentation generation."""

    chapters: Sequence[Path]
    destination_dirname: str
    prompt_template: str | None = None


@dataclass(slots=True)
class DocumentOutcome:
    """Outcome of documentation generation for a batch of chapters."""

    written: list[tuple[Path, Path]]
    failures: list[tuple[Path, str]]

    @property
    def success(self) -> bool:
        return not self.failures

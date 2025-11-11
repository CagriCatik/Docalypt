"""Domain services containing pure business logic."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List, Pattern

from .models import Chapter, ChapterDocument, SplitTranscript


@dataclass(slots=True)
class TranscriptParser:
    """Parse raw transcript text into structured chapter documents."""

    marker_pattern: Pattern[str]

    def split(self, transcript_text: str) -> SplitTranscript:
        header, body = self._split_sections(transcript_text)
        chapters = self._parse_chapter_metadata(header)
        buckets = {chapter.index: [] for chapter in chapters}

        parts = self.marker_pattern.split(body)
        if len(parts) <= 1:
            raise ValueError("No timestamp markers found in transcript body")

        for index in range(1, len(parts), 2):
            timestamp = _parse_hhmmss(parts[index])
            snippet = parts[index + 1].strip()
            chapter = _find_chapter_for_timestamp(timestamp, chapters)
            if snippet:
                buckets[chapter.index].append(snippet)

        documents: List[ChapterDocument] = []
        for chapter in chapters:
            content_lines = [f"# {chapter.title}", ""]
            content_lines.extend(buckets.get(chapter.index, []))
            documents.append(
                ChapterDocument(
                    chapter=chapter,
                    content="\n\n".join(content_lines).strip() + "\n",
                )
            )
        return SplitTranscript(documents=documents)

    def _split_sections(self, transcript_text: str) -> tuple[str, str]:
        try:
            header, body = transcript_text.split("\n\nTranscript:", 1)
        except ValueError as exc:  # pragma: no cover - invalid format guard
            raise ValueError("Transcript missing 'Transcript:' separator") from exc
        return header, body

    def _parse_chapter_metadata(self, header: str) -> List[Chapter]:
        parsed: List[Chapter] = []
        for line in header.splitlines():
            match = re.match(r"^(\d{2}:\d{2}:\d{2})\s*[-–]\s*(.+)$", line.strip())
            if not match:
                continue
            timestamp, title = match.groups()
            parsed.append(
                Chapter(
                    index=len(parsed) + 1,
                    title=title.strip(),
                    timestamp=_parse_hhmmss(timestamp),
                )
            )
        parsed.sort(key=lambda chapter: chapter.timestamp)
        for new_index, chapter in enumerate(parsed, start=1):
            parsed[new_index - 1] = Chapter(
                index=new_index,
                title=chapter.title,
                timestamp=chapter.timestamp,
            )
        return parsed


def _parse_hhmmss(value: str) -> int:
    parts = [int(part) for part in value.split(":")]
    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds
    hours, minutes, seconds = parts
    return hours * 3600 + minutes * 60 + seconds


def _find_chapter_for_timestamp(timestamp: int, chapters: Iterable[Chapter]) -> Chapter:
    eligible = [chapter for chapter in chapters if chapter.timestamp <= timestamp]
    if not eligible:
        return next(iter(chapters))  # pragma: no cover - should not happen with data
    return eligible[-1]


__all__ = ["TranscriptParser"]

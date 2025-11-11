"""Markdown transcript splitting utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Callable, Iterable, List, Optional, Sequence

from .config import AppConfig, load_config

ProgressCallback = Callable[[int, int], None]
TextHook = Callable[[str], str]
FileHook = Callable[[Path], None]


def _parse_hhmmss(value: str) -> int:
    parts = [int(part) for part in value.split(":")]
    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds
    hours, minutes, seconds = parts
    return hours * 3600 + minutes * 60 + seconds


@dataclass(slots=True)
class Chapter:
    timestamp: int
    title: str


@dataclass(slots=True)
class SplitResult:
    chapters: Sequence[Path]
    html_path: Path | None = None


@dataclass(slots=True)
class TranscriptSplitter:
    """Split transcript markdown files into chapter documents."""

    input_path: Path
    output_dir: Optional[Path] = None
    marker_regex: Optional[str] = None
    on_progress: ProgressCallback | None = None
    pre_split_hooks: Iterable[TextHook] = field(default_factory=list)
    post_split_hooks: Iterable[FileHook] = field(default_factory=list)
    config: AppConfig = field(init=False)

    def __post_init__(self) -> None:
        self.config = load_config()
        self.output_dir = (
            Path(self.output_dir).expanduser().resolve()
            if self.output_dir
            else self.config.output_dir
        )
        pattern = self.marker_regex or self.config.marker_regex
        self._marker_pattern = re.compile(pattern)
        self._chapter_count = 0

    # Public API ---------------------------------------------------------
    def split(self, export_html: bool = False) -> int:
        result = self._split_internal(export_html=export_html)
        self._chapter_count = len(result.chapters)
        return self._chapter_count

    # Internal helpers ---------------------------------------------------
    def _split_internal(self, export_html: bool) -> SplitResult:
        text = self.input_path.read_text(encoding="utf-8")
        try:
            header, body = text.split("\n\nTranscript:", 1)
        except ValueError as exc:  # pragma: no cover - invalid format guard
            raise ValueError("Transcript missing 'Transcript:' separator") from exc

        chapters = self._parse_chapters(header)
        processed_body = self._apply_pre_hooks(body)
        chapter_files = self._write_chapters(chapters, processed_body)

        html_path = None
        if export_html:
            html_path = self._write_html_index(chapters, chapter_files)

        return SplitResult(chapters=chapter_files, html_path=html_path)

    def _parse_chapters(self, header: str) -> List[Chapter]:
        parsed: List[Chapter] = []
        for line in header.splitlines():
            match = re.match(r"^(\d{2}:\d{2}:\d{2})\s*[-–]\s*(.+)$", line.strip())
            if not match:
                continue
            timestamp, title = match.groups()
            parsed.append(Chapter(timestamp=_parse_hhmmss(timestamp), title=title.strip()))
        parsed.sort(key=lambda chapter: chapter.timestamp)
        return parsed

    def _apply_pre_hooks(self, body: str) -> str:
        updated = body
        for hook in self.pre_split_hooks:
            updated = hook(updated)
        return updated

    def _write_chapters(self, chapters: Sequence[Chapter], body: str) -> List[Path]:
        buckets: dict[str, list[str]] = {chapter.title: [] for chapter in chapters}
        parts = self._marker_pattern.split(body)
        if len(parts) <= 1:
            raise ValueError("No timestamp markers found in transcript body")

        total = (len(parts) - 1) // 2
        progress_counter = 0

        for index in range(1, len(parts), 2):
            progress_counter += 1
            ts_value = parts[index]
            snippet = parts[index + 1].strip()
            timestamp = _parse_hhmmss(ts_value)
            owning_title = self._find_chapter_title(timestamp, chapters)
            buckets[owning_title].append(snippet)
            if self.on_progress:
                self.on_progress(progress_counter, total)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        written_paths: List[Path] = []
        for position, chapter in enumerate(chapters, start=1):
            snippets = buckets.get(chapter.title, [])
            slug = re.sub(r"[^\w-]", "_", chapter.title.lower().replace(" ", "_"))
            filename = f"{position:02d}_{slug}.md"
            destination = self.output_dir / filename
            content_lines = [f"# {chapter.title}", ""] + [snippet for snippet in snippets if snippet]
            destination.write_text("\n\n".join(content_lines).strip() + "\n", encoding="utf-8")
            for hook in self.post_split_hooks:
                hook(destination)
            written_paths.append(destination)
        return written_paths

    def _find_chapter_title(self, timestamp: int, chapters: Sequence[Chapter]) -> str:
        eligible = [chapter for chapter in chapters if chapter.timestamp <= timestamp]
        if not eligible:
            return chapters[0].title
        return eligible[-1].title

    def _write_html_index(self, chapters: Sequence[Chapter], files: Sequence[Path]) -> Path:
        html_lines = ["<html><body>", "<h1>Transcript Chapters</h1>", "<ul>"]
        for chapter, path in zip(chapters, files):
            content = path.read_text(encoding="utf-8")
            html_lines.append(f"<li><h2>{chapter.title}</h2><pre>{content}</pre></li>")
        html_lines.extend(["</ul>", "</body></html>"])
        html_path = self.output_dir / "index.html"
        html_path.write_text("\n".join(html_lines), encoding="utf-8")
        return html_path


__all__ = ["Chapter", "SplitResult", "TranscriptSplitter"]

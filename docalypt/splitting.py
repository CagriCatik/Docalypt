"""Markdown transcript splitting utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Optional, Sequence

from docalypt.application.split_transcript import SplitTranscriptUseCase
from docalypt.domain.services import TranscriptParser
from docalypt.infrastructure.config.toml_loader import AppConfig, load_app_config
from docalypt.infrastructure.storage.filesystem import FileSystemChapterRepository

ProgressCallback = Callable[[int, int], None]
TextHook = Callable[[str], str]
FileHook = Callable[[Path], None]


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
    _use_case: SplitTranscriptUseCase = field(init=False)

    def __post_init__(self) -> None:
        self.config = load_app_config()
        output_dir = (
            Path(self.output_dir).expanduser().resolve()
            if self.output_dir
            else self.config.output_dir
        )
        self.output_dir = output_dir
        pattern = re.compile(self.marker_regex or self.config.marker_regex)
        parser = TranscriptParser(marker_pattern=pattern)
        repository = FileSystemChapterRepository(
            output_dir=output_dir,
            html_template_path=self.config.html_template,
        )
        self._use_case = SplitTranscriptUseCase(
            parser=parser,
            repository=repository,
            progress_reporter=self.on_progress,
        )

    # Public API ---------------------------------------------------------
    def split(self, export_html: bool = False) -> int:
        result = self._split_internal(export_html=export_html)
        return len(result.chapters)

    # Internal helpers ---------------------------------------------------
    def _split_internal(self, export_html: bool) -> SplitResult:
        text = self.input_path.read_text(encoding="utf-8")
        try:
            header, body = text.split("\n\nTranscript:", 1)
            processed_body = body
            for hook in self.pre_split_hooks:
                processed_body = hook(processed_body)
            processed_text = f"{header}\n\nTranscript:{processed_body}"
        except ValueError:
            processed_text = text
            for hook in self.pre_split_hooks:
                processed_text = hook(processed_text)

        # Allow callers to mutate the progress callback between runs.
        self._use_case.progress_reporter = self.on_progress

        split_result, written_paths, html_path = self._use_case.execute(
            input_path=self.input_path,
            export_html=export_html,
            transcript_text=processed_text,
        )

        for path in written_paths:
            for hook in self.post_split_hooks:
                hook(path)

        return SplitResult(chapters=written_paths, html_path=html_path)


__all__ = ["SplitResult", "TranscriptSplitter"]

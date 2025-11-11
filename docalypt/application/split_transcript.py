"""Application service coordinating transcript splitting."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from docalypt.domain.models import SplitTranscript
from docalypt.domain.services import TranscriptParser

from .protocols import ChapterRepository, ProgressReporter


@dataclass(slots=True)
class SplitTranscriptUseCase:
    """Read a transcript file and persist the resulting chapter documents."""

    parser: TranscriptParser
    repository: ChapterRepository
    progress_reporter: ProgressReporter | None = None

    def execute(
        self,
        input_path: Path,
        export_html: bool = False,
        transcript_text: str | None = None,
    ) -> tuple[SplitTranscript, Sequence[Path], Path | None]:
        text = transcript_text or input_path.read_text(encoding="utf-8")
        split_result = self.parser.split(text)

        total = len(split_result.documents)
        if self.progress_reporter:
            self.progress_reporter(0, total)

        written_paths: list[Path] = []
        html_path: Path | None = None
        # Persist documents sequentially to surface meaningful progress updates.
        for index, document in enumerate(split_result.documents, start=1):
            saved, _ = self.repository.save_documents([document], export_html=False)
            written_paths.extend(saved)
            if self.progress_reporter:
                self.progress_reporter(index, total)

        if export_html:
            html_path = self.repository.render_html_index(split_result.documents)

        if self.progress_reporter:
            self.progress_reporter(total, total)

        return split_result, written_paths, html_path


__all__ = ["SplitTranscriptUseCase"]

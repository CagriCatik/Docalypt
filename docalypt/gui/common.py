"""Shared Qt helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, Sequence

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QTextEdit

from ..documentation import (
    DocumentGenerationRequest,
    DocumentGenerationResult,
    generate_documentation,
)
from ..splitting import TranscriptSplitter


class QtLogHandler(logging.Handler):
    """Route Python logs into a QTextEdit widget."""

    def __init__(self, widget: QTextEdit):
        super().__init__()
        self.widget = widget

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        self.widget.append(message)


class SplitWorker(QObject):
    finished = Signal(int)
    error = Signal(str)
    progress = Signal(int)

    def __init__(self, splitter: TranscriptSplitter):
        super().__init__()
        self.splitter = splitter

    def run(self) -> None:
        try:
            def on_progress(current: int, total: int) -> None:
                if total:
                    self.progress.emit(int(current / total * 100))

            self.splitter.on_progress = on_progress
            count = self.splitter.split()
            self.finished.emit(count)
        except Exception as exc:  # pragma: no cover - runtime guard
            self.error.emit(str(exc))


class DocumentationWorker(QObject):
    finished = Signal(DocumentGenerationResult)
    chapter_done = Signal(str, str)
    chapter_failed = Signal(str, str)

    def __init__(self, request: DocumentGenerationRequest):
        super().__init__()
        self.request = request

    def run(self) -> None:
        result = generate_documentation(self.request)
        for written in result.written:
            self.chapter_done.emit(written.stem.replace(".docs", ""), str(written))
        for chapter, error in result.failures:
            self.chapter_failed.emit(chapter.name, error)
        self.finished.emit(result)


__all__ = [
    "DocumentationWorker",
    "QtLogHandler",
    "SplitWorker",
]

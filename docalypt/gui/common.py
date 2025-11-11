"""Shared Qt helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QTextEdit

from ..documentation import DOCUMENTATION_SUBDIR, DocumentOutcome, generate_documentation
from ..ollama import OllamaError, OllamaSettings, list_local_models
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
    finished = Signal(DocumentOutcome)
    chapter_done = Signal(str, str)
    chapter_failed = Signal(str, str)

    def __init__(
        self,
        chapters: Sequence[Path],
        settings: OllamaSettings,
        prompt_template: str | None = None,
        destination_dirname: str = DOCUMENTATION_SUBDIR,
    ):
        super().__init__()
        self.chapters = chapters
        self.settings = settings
        self.prompt_template = prompt_template
        self.destination_dirname = destination_dirname

    def run(self) -> None:
        result = generate_documentation(
            chapters=self.chapters,
            settings=self.settings,
            destination_dirname=self.destination_dirname,
            prompt_template=self.prompt_template,
        )
        for chapter, destination in result.written:
            self.chapter_done.emit(chapter.name, str(destination))
        for chapter, error in result.failures:
            self.chapter_failed.emit(chapter.name, error)
        self.finished.emit(result)


class ModelListWorker(QObject):
    finished = Signal(list)
    failed = Signal(str)

    def __init__(self, endpoint: str):
        super().__init__()
        self.endpoint = endpoint

    def run(self) -> None:
        try:
            models = list_local_models(self.endpoint)
            self.finished.emit(models)
        except OllamaError as exc:
            self.failed.emit(str(exc))
        except Exception as exc:  # pragma: no cover - safety net
            self.failed.emit(str(exc))


__all__ = [
    "DocumentationWorker",
    "ModelListWorker",
    "QtLogHandler",
    "SplitWorker",
]

"""Shared Qt helpers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QTextEdit

from ..documentation import (
    DocumentGenerationRequest,
    DocumentGenerationResult,
    generate_documentation,
)
from ..llm import LLMError, LLMSettings, list_models


class QtLogHandler(logging.Handler):
    """Route Python logs into a QTextEdit widget."""

    def __init__(self, widget: QTextEdit):
        super().__init__()
        self.widget = widget

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        self.widget.append(message)


class DocumentationWorker(QObject):
    finished = Signal(DocumentGenerationResult)
    chapter_done = Signal(str, str)
    chapter_failed = Signal(str, str)

    def __init__(self, request: DocumentGenerationRequest):
        super().__init__()
        self.request = request

    def run(self) -> None:
        result = generate_documentation(self.request)
        for chapter, destination in result.written:
            self.chapter_done.emit(chapter.name, str(destination))
        for chapter, error in result.failures:
            self.chapter_failed.emit(chapter.name, error)
        self.finished.emit(result)


class ModelListWorker(QObject):
    finished = Signal(list)
    failed = Signal(str)

    def __init__(self, settings: LLMSettings):
        super().__init__()
        self.settings = settings

    def run(self) -> None:
        try:
            models = list_models(self.settings)
            self.finished.emit(models)
        except LLMError as exc:
            self.failed.emit(str(exc))
        except Exception as exc:  # pragma: no cover - safety net
            self.failed.emit(str(exc))


__all__ = [
    "DocumentationWorker",
    "ModelListWorker",
    "QtLogHandler",
]

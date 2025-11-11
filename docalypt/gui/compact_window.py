"""Compact PySide6 GUI for Docalypt."""

from __future__ import annotations

import logging
from dataclasses import replace
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..documentation import DocumentGenerationRequest, collect_chapter_files
from ..llm import settings_from_env
from ..splitting import TranscriptSplitter
from .common import DocumentationWorker, QtLogHandler, SplitWorker

DEFAULT_MODEL = "llama3"


class CompactWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Docalypt (Compact)")
        self.resize(520, 280)

        self.logger = logging.getLogger("docalypt.gui.compact")
        self.logger.setLevel(logging.INFO)

        self._llm_defaults = settings_from_env()
        self._input: Optional[Path] = None
        self._output_dir: Path = Path.cwd() / "chapters"
        self._split_thread: Optional[QThread] = None
        self._doc_thread: Optional[QThread] = None

        self._build_ui()
        self._apply_defaults()
        self._connect_signals()
        self._update_controls()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        input_row = QHBoxLayout()
        self.input_edit = QLineEdit(readOnly=True)
        self.input_btn = QPushButton("Browse…")
        input_row.addWidget(QLabel("Input"))
        input_row.addWidget(self.input_edit, stretch=1)
        input_row.addWidget(self.input_btn)

        output_row = QHBoxLayout()
        self.output_edit = QLineEdit(str(self._output_dir), readOnly=True)
        self.output_btn = QPushButton("Output…")
        output_row.addWidget(QLabel("Output"))
        output_row.addWidget(self.output_edit, stretch=1)
        output_row.addWidget(self.output_btn)

        self.split_btn = QPushButton("Split transcript")

        self.enable_ollama = QCheckBox(
            "Generate documentation with configured LLM"
        )
        self.model_edit = QLineEdit(DEFAULT_MODEL)
        self.model_edit.setPlaceholderText("Model name (e.g. llama3)")

        ollama_row = QHBoxLayout()
        ollama_row.addWidget(QLabel("Model"))
        ollama_row.addWidget(self.model_edit, stretch=1)

        self.log_area = QTextEdit(readOnly=True)

        layout.addLayout(input_row)
        layout.addLayout(output_row)
        layout.addWidget(self.split_btn)
        layout.addWidget(self.enable_ollama)
        layout.addLayout(ollama_row)
        layout.addWidget(self.log_area, stretch=1)

        handler = QtLogHandler(self.log_area)
        handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%H:%M:%S"))
        self.logger.addHandler(handler)

    def _apply_defaults(self) -> None:
        model = self._llm_defaults.model or DEFAULT_MODEL
        self.model_edit.setText(model)

    def _connect_signals(self) -> None:
        self.input_btn.clicked.connect(self._select_input)
        self.output_btn.clicked.connect(self._select_output)
        self.split_btn.clicked.connect(self._start_split)
        self.enable_ollama.stateChanged.connect(self._update_controls)
        self.model_edit.textChanged.connect(self._update_controls)

    def _select_input(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select transcript", str(Path.cwd()), "Markdown files (*.md)"
        )
        if path:
            self._input = Path(path)
            self.input_edit.setText(path)
            self.logger.info("Loaded input %s", path)

    def _select_output(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self, "Select output", str(self._output_dir)
        )
        if directory:
            self._output_dir = Path(directory)
            self.output_edit.setText(directory)
            self.logger.info("Output directory set to %s", directory)

    def _start_split(self) -> None:
        if not self._input:
            self.logger.error("No transcript selected")
            return
        self.split_btn.setEnabled(False)
        self.logger.info("Splitting transcript…")

        splitter = TranscriptSplitter(self._input, self._output_dir)
        self._split_thread = QThread()
        worker = SplitWorker(splitter)
        worker.moveToThread(self._split_thread)
        self._split_thread.started.connect(worker.run)
        worker.finished.connect(lambda count: self._on_split_finished(count, worker))
        worker.error.connect(lambda message: self._on_split_error(message, worker))
        self._split_thread.start()

    def _on_split_finished(self, count: int, worker: SplitWorker) -> None:
        self.logger.info("Split finished: %d chapters", count)
        self.split_btn.setEnabled(True)
        if self.enable_ollama.isChecked():
            self._start_documentation()
        if self._split_thread:
            self._split_thread.quit()
            self._split_thread.wait()
            self._split_thread = None
        worker.deleteLater()

    def _on_split_error(self, message: str, worker: SplitWorker) -> None:
        self.logger.error("Split failed: %s", message)
        self.split_btn.setEnabled(True)
        if self._split_thread:
            self._split_thread.quit()
            self._split_thread.wait()
            self._split_thread = None
        worker.deleteLater()

    def _start_documentation(self) -> None:
        model = self.model_edit.text().strip()
        if not model:
            self.logger.error("Documentation skipped: missing model name")
            return
        chapters = collect_chapter_files(self._output_dir)
        if not chapters:
            self.logger.warning("No chapters found for documentation")
            return

        settings = replace(self._llm_defaults, model=model)
        request = DocumentGenerationRequest(chapters=chapters, settings=settings)
        provider = (self._llm_defaults.provider or "ollama").capitalize()
        self.logger.info(
            "Generating documentation with %s (%s) for %d chapters",
            model,
            provider,
            len(chapters),
        )

        self.enable_ollama.setEnabled(False)
        self.model_edit.setEnabled(False)

        self._doc_thread = QThread()
        worker = DocumentationWorker(request)
        worker.moveToThread(self._doc_thread)
        self._doc_thread.started.connect(worker.run)
        worker.chapter_done.connect(
            lambda chapter, output: self.logger.info("Documented %s → %s", chapter, output)
        )
        worker.chapter_failed.connect(
            lambda chapter, error: self.logger.error("Failed %s: %s", chapter, error)
        )
        worker.finished.connect(lambda _: self._on_doc_finished(worker))
        self._doc_thread.start()

    def _on_doc_finished(self, worker: DocumentationWorker) -> None:
        self.logger.info("Documentation finished")
        self.enable_ollama.setEnabled(True)
        self.model_edit.setEnabled(True)
        if self._doc_thread:
            self._doc_thread.quit()
            self._doc_thread.wait()
            self._doc_thread = None
        worker.deleteLater()

    def _update_controls(self) -> None:
        enabled = self.enable_ollama.isChecked()
        self.model_edit.setEnabled(enabled)
        if enabled and not self.model_edit.text().strip():
            self.split_btn.setToolTip("Provide a model name or disable generation")
        else:
            self.split_btn.setToolTip("")

    def closeEvent(self, event) -> None:  # noqa: N802
        for thread in (self._split_thread, self._doc_thread):
            if thread and thread.isRunning():
                thread.quit()
                thread.wait(500)
        super().closeEvent(event)


def run() -> None:
    app = QApplication.instance() or QApplication([])
    window = CompactWindow()
    window.show()
    app.exec()

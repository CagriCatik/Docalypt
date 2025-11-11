# File: compact_gui.py
import sys
import logging
from pathlib import Path
from typing import Optional, Sequence

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from splitter import TranscriptSplitter
from ollama_helper import OllamaGenerationError, OllamaSettings, document_chapter

DEFAULT_MODEL_NAME = "llama3"


class QtLogHandler(logging.Handler):
    def __init__(self, widget: QTextEdit):
        super().__init__()
        self.widget = widget

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.widget.append(msg)


class SplitWorker(QObject):
    finished = Signal(int)
    error = Signal(str)

    def __init__(self, splitter: TranscriptSplitter):
        super().__init__()
        self._splitter = splitter

    def run(self) -> None:
        try:
            count = self._splitter.split()
            self.finished.emit(count)
        except Exception as exc:
            self.error.emit(str(exc))


class DocumentationWorker(QObject):
    finished = Signal()
    chapter_done = Signal(str, str)
    chapter_failed = Signal(str, str)

    def __init__(self, chapters: Sequence[Path], settings: OllamaSettings):
        super().__init__()
        self._chapters = list(chapters)
        self._settings = settings

    def run(self) -> None:
        for chapter in self._chapters:
            try:
                output = document_chapter(chapter, self._settings)
            except OllamaGenerationError as exc:
                self.chapter_failed.emit(chapter.name, str(exc))
                continue
            except Exception as exc:  # pragma: no cover - defensive
                self.chapter_failed.emit(chapter.name, str(exc))
                continue
            self.chapter_done.emit(chapter.name, str(output))
        self.finished.emit()


class CompactWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown Splitter (Compact)")
        self.resize(480, 260)
        self.current_path: Optional[Path] = None
        self.output_dir: Path = Path.cwd() / "chapters"
        self.thread: Optional[QThread] = None
        self.worker: Optional[SplitWorker] = None
        self.doc_thread: Optional[QThread] = None
        self.doc_worker: Optional[DocumentationWorker] = None

        layout = QVBoxLayout(self)

        # Input controls
        input_row = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("Select transcript markdown…")
        self.input_edit.setReadOnly(True)
        self.input_btn = QPushButton("Browse…")
        input_row.addWidget(QLabel("Input"))
        input_row.addWidget(self.input_edit)
        input_row.addWidget(self.input_btn)

        output_row = QHBoxLayout()
        self.output_edit = QLineEdit(str(self.output_dir))
        self.output_edit.setReadOnly(True)
        self.output_btn = QPushButton("Output…")
        output_row.addWidget(QLabel("Output"))
        output_row.addWidget(self.output_edit)
        output_row.addWidget(self.output_btn)

        self.split_btn = QPushButton("Split Transcript")

        # Ollama options
        self.enable_ollama = QCheckBox("Generate documentation with Ollama")
        self.model_edit = QLineEdit(DEFAULT_MODEL_NAME)
        self.model_edit.setPlaceholderText("Model name (e.g. llama3)")

        ollama_row = QHBoxLayout()
        ollama_row.addWidget(QLabel("Model"))
        ollama_row.addWidget(self.model_edit)

        # Log area
        self.log_area = QTextEdit(readOnly=True)

        layout.addLayout(input_row)
        layout.addLayout(output_row)
        layout.addWidget(self.split_btn)
        layout.addWidget(self.enable_ollama)
        layout.addLayout(ollama_row)
        layout.addWidget(self.log_area)

        # Logging
        self.logger = logging.getLogger("compact_splitter")
        self.logger.setLevel(logging.DEBUG)
        handler = QtLogHandler(self.log_area)
        handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%H:%M:%S"))
        self.logger.addHandler(handler)

        # Connections
        self.input_btn.clicked.connect(self.select_input)
        self.output_btn.clicked.connect(self.select_output)
        self.split_btn.clicked.connect(self.start_split)
        self.enable_ollama.stateChanged.connect(self.update_doc_controls)
        self.model_edit.textChanged.connect(self.update_doc_controls)

        self.update_doc_controls()

    # ------------------------------------------------------------------
    def select_input(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Transcript", str(Path.cwd()), "Markdown Files (*.md)"
        )
        if path:
            self.current_path = Path(path)
            self.input_edit.setText(path)
            self.logger.info("Loaded input: %s", path)

    def select_output(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self, "Select Output", str(self.output_dir)
        )
        if directory:
            self.output_dir = Path(directory)
            self.output_edit.setText(directory)
            self.logger.info("Output directory set to: %s", directory)

    def start_split(self) -> None:
        if not self.current_path:
            self.logger.error("No input file selected.")
            return
        self.split_btn.setEnabled(False)
        self.logger.info("Splitting transcript…")

        splitter = TranscriptSplitter(self.current_path, self.output_dir)
        self.thread = QThread()
        self.worker = SplitWorker(splitter)
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.on_split_complete)
        self.worker.error.connect(self.on_split_error)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def on_split_complete(self, count: int) -> None:
        self.logger.info("Split finished: %d chapters", count)
        if self.thread:
            self.thread.quit()
            self.thread.wait()
            self.thread = None
            self.worker = None
        self.split_btn.setEnabled(True)
        if self.enable_ollama.isChecked():
            self.start_documentation()

    def on_split_error(self, message: str) -> None:
        self.logger.error("Split failed: %s", message)
        if self.thread:
            self.thread.quit()
            self.thread.wait()
            self.thread = None
            self.worker = None
        self.split_btn.setEnabled(True)

    def start_documentation(self) -> None:
        model = self.model_edit.text().strip()
        if not model:
            self.logger.error("Documentation skipped: no model configured.")
            return
        chapters = [
            path
            for path in sorted(self.output_dir.glob("*.md"))
            if not path.name.endswith(".docs.md")
        ]
        if not chapters:
            self.logger.warning("No chapter files found for documentation.")
            return

        settings = OllamaSettings(
            model=model,
            temperature=0.2,
            max_tokens=800,
            top_p=0.9,
        )
        self.logger.info(
            "Generating documentation with %s for %d chapters…",
            model,
            len(chapters),
        )
        self.enable_ollama.setEnabled(False)
        self.model_edit.setEnabled(False)

        self.doc_thread = QThread()
        self.doc_worker = DocumentationWorker(chapters, settings)
        self.doc_worker.moveToThread(self.doc_thread)
        self.doc_thread.started.connect(self.doc_worker.run)
        self.doc_worker.finished.connect(self.on_docs_finished)
        self.doc_worker.chapter_done.connect(self.on_doc_success)
        self.doc_worker.chapter_failed.connect(self.on_doc_failed)
        self.doc_thread.start()

    def on_docs_finished(self) -> None:
        self.logger.info("Documentation finished.")
        if self.doc_thread:
            self.doc_thread.quit()
            self.doc_thread.wait()
            self.doc_thread = None
            self.doc_worker = None
        self.enable_ollama.setEnabled(True)
        self.model_edit.setEnabled(self.enable_ollama.isChecked())

    def on_doc_success(self, chapter: str, output: str) -> None:
        self.logger.info("Documented %s -> %s", chapter, output)

    def on_doc_failed(self, chapter: str, error: str) -> None:
        self.logger.error("Failed to document %s: %s", chapter, error)

    def update_doc_controls(self) -> None:
        enabled = self.enable_ollama.isChecked()
        self.model_edit.setEnabled(enabled)
        if enabled and not self.model_edit.text().strip():
            self.split_btn.setToolTip("Provide a model name or disable Ollama generation.")
        else:
            self.split_btn.setToolTip("")

    def closeEvent(self, event):  # noqa: N802 - Qt signature
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait(500)
        if self.doc_thread and self.doc_thread.isRunning():
            self.doc_thread.quit()
            self.doc_thread.wait(500)
        super().closeEvent(event)


def main() -> None:
    app = QApplication(sys.argv)
    window = CompactWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

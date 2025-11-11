"""Main PySide6 GUI for Docalypt."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QDesktopServices, QDragEnterEvent, QDropEvent, QIcon, QIntValidator
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QAbstractItemView,
    QMessageBox,
)

from ..documentation import (
    DocumentGenerationRequest,
    OllamaSettings,
    collect_chapter_files,
)
from ..splitting import TranscriptSplitter
from .common import DocumentationWorker, QtLogHandler, SplitWorker

DEFAULT_MODEL = "llama3"


class MainWindow(QMainWindow):
    generation_finished = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Docalypt • Transcript Splitter & Doc Generator")
        self.resize(860, 540)
        self.setAcceptDrops(True)

        self.logger = logging.getLogger("docalypt.gui")
        self.logger.setLevel(logging.INFO)

        self._input_path: Optional[Path] = None
        self._output_dir: Path = Path.cwd() / "chapters"
        self._split_thread: Optional[QThread] = None
        self._doc_thread: Optional[QThread] = None

        self._build_ui()
        self._connect_signals()
        self._refresh_chapter_list()
        self._update_doc_controls()

    # UI -----------------------------------------------------------------
    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        toolbar = QHBoxLayout()
        self.open_btn = QPushButton("📂 Open Markdown…")
        self.output_btn = QPushButton("📁 Output Folder…")
        self.split_btn = QPushButton("🚀 Split Transcript")
        self.open_folder_btn = QPushButton("📂 Reveal Output")
        self.clear_log_btn = QPushButton("🧹 Clear Log")
        self.save_log_btn = QPushButton("💾 Save Log…")
        for button in (
            self.open_btn,
            self.output_btn,
            self.split_btn,
            self.open_folder_btn,
            self.clear_log_btn,
            self.save_log_btn,
        ):
            toolbar.addWidget(button)
        layout.addLayout(toolbar)

        self.progress = QProgressBar()
        self.progress.hide()
        layout.addWidget(self.progress)

        self.log_area = QTextEdit(readOnly=True)
        layout.addWidget(self.log_area, stretch=1)

        self.ollama_group = QGroupBox("LLM / Ollama")
        ollama_layout = QVBoxLayout(self.ollama_group)

        self.enable_ollama = QCheckBox("Enable documentation generation with Ollama")
        ollama_layout.addWidget(self.enable_ollama)

        form = QFormLayout()
        self.model_edit = QLineEdit(DEFAULT_MODEL)
        form.addRow("Model", self.model_edit)

        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setDecimals(2)
        self.temperature_spin.setSingleStep(0.05)
        self.temperature_spin.setValue(0.2)
        form.addRow("Temperature", self.temperature_spin)

        self.top_p_spin = QDoubleSpinBox()
        self.top_p_spin.setRange(0.0, 1.0)
        self.top_p_spin.setDecimals(2)
        self.top_p_spin.setSingleStep(0.05)
        self.top_p_spin.setValue(0.9)
        form.addRow("Top_p", self.top_p_spin)

        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(16, 8192)
        self.max_tokens_spin.setValue(800)
        form.addRow("Max tokens", self.max_tokens_spin)

        ollama_layout.addLayout(form)

        self.chapter_list = QListWidget()
        self.chapter_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.chapter_list.setMinimumHeight(160)
        ollama_layout.addWidget(QLabel("Chapters ready for documentation"))
        ollama_layout.addWidget(self.chapter_list)

        doc_toolbar = QHBoxLayout()
        self.select_all_btn = QPushButton("Select all")
        self.generate_docs_btn = QPushButton("Generate documentation")
        doc_toolbar.addWidget(self.select_all_btn)
        doc_toolbar.addWidget(self.generate_docs_btn)
        ollama_layout.addLayout(doc_toolbar)

        layout.insertWidget(2, self.ollama_group)

        handler = QtLogHandler(self.log_area)
        handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%H:%M:%S"))
        self.logger.addHandler(handler)

    def _connect_signals(self) -> None:
        self.open_btn.clicked.connect(self._open_file)
        self.output_btn.clicked.connect(self._select_output)
        self.split_btn.clicked.connect(self._start_split)
        self.open_folder_btn.clicked.connect(self._reveal_output)
        self.clear_log_btn.clicked.connect(self.log_area.clear)
        self.save_log_btn.clicked.connect(self._save_log)
        self.enable_ollama.stateChanged.connect(self._update_doc_controls)
        self.model_edit.textChanged.connect(self._update_doc_controls)
        self.chapter_list.itemSelectionChanged.connect(self._update_doc_controls)
        self.select_all_btn.clicked.connect(self._select_all)
        self.generate_docs_btn.clicked.connect(self._start_documentation)

    # Drag & drop --------------------------------------------------------
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if not urls:
            return
        path = Path(urls[0].toLocalFile())
        if path.suffix.lower() == ".md":
            self._load_markdown(path)

    # Actions ------------------------------------------------------------
    def _open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select transcript",
            str(Path.cwd()),
            "Markdown files (*.md)",
        )
        if path:
            self._load_markdown(Path(path))

    def _load_markdown(self, path: Path) -> None:
        self._input_path = path
        self.logger.info("Loaded input: %s", path)

    def _select_output(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select output directory",
            str(self._output_dir),
        )
        if directory:
            self._output_dir = Path(directory)
            self.logger.info("Output directory set to %s", directory)
            self._refresh_chapter_list()

    def _start_split(self) -> None:
        if not self._input_path:
            QMessageBox.warning(self, "Missing input", "Select a transcript to split first.")
            return
        self.logger.info("Splitting transcript…")
        self.split_btn.setEnabled(False)
        self.progress.setValue(0)
        self.progress.show()

        splitter = TranscriptSplitter(self._input_path, self._output_dir)
        self._split_thread = QThread()
        worker = SplitWorker(splitter)
        worker.moveToThread(self._split_thread)
        self._split_thread.started.connect(worker.run)
        worker.progress.connect(self.progress.setValue)
        worker.finished.connect(lambda count: self._on_split_finished(count, worker))
        worker.error.connect(lambda message: self._on_split_error(message, worker))
        self._split_thread.start()

    def _on_split_finished(self, count: int, worker: SplitWorker) -> None:
        self.logger.info("Split complete: %d chapters", count)
        self.progress.hide()
        self.split_btn.setEnabled(True)
        self._refresh_chapter_list()
        if self._split_thread:
            self._split_thread.quit()
            self._split_thread.wait()
            self._split_thread = None
        worker.deleteLater()

    def _on_split_error(self, message: str, worker: SplitWorker) -> None:
        self.logger.error("Split failed: %s", message)
        self.progress.hide()
        self.split_btn.setEnabled(True)
        if self._split_thread:
            self._split_thread.quit()
            self._split_thread.wait()
            self._split_thread = None
        worker.deleteLater()

    def _reveal_output(self) -> None:
        QDesktopServices.openUrl(self._output_dir.as_uri())

    def _save_log(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save log",
            "docalypt.log",
            "Text files (*.txt)",
        )
        if path:
            Path(path).write_text(self.log_area.toPlainText(), encoding="utf-8")
            self.logger.info("Log saved to %s", path)

    # Documentation ------------------------------------------------------
    def _refresh_chapter_list(self) -> None:
        self.chapter_list.clear()
        if not self._output_dir.exists():
            self._update_doc_controls()
            return
        for chapter in collect_chapter_files(self._output_dir):
            item = QListWidgetItem(chapter.name)
            item.setData(Qt.UserRole, chapter)
            self.chapter_list.addItem(item)
        self._update_doc_controls()

    def _select_all(self) -> None:
        for index in range(self.chapter_list.count()):
            self.chapter_list.item(index).setSelected(True)
        self._update_doc_controls()

    def _selected_chapters(self) -> list[Path]:
        selected: list[Path] = []
        for item in self.chapter_list.selectedItems():
            chapter = item.data(Qt.UserRole)
            if isinstance(chapter, Path):
                selected.append(chapter)
        return selected

    def _gather_settings(self) -> OllamaSettings:
        return OllamaSettings(
            model=self.model_edit.text().strip(),
            temperature=float(self.temperature_spin.value()),
            top_p=float(self.top_p_spin.value()),
            max_tokens=int(self.max_tokens_spin.value()),
        )

    def _update_doc_controls(self) -> None:
        enabled = self.enable_ollama.isChecked()
        has_model = bool(self.model_edit.text().strip())
        selected = bool(self._selected_chapters())
        has_chapters = self.chapter_list.count() > 0

        for widget in (
            self.model_edit,
            self.temperature_spin,
            self.top_p_spin,
            self.max_tokens_spin,
            self.chapter_list,
            self.select_all_btn,
        ):
            widget.setEnabled(enabled)

        self.select_all_btn.setEnabled(enabled and has_chapters)
        self.generate_docs_btn.setEnabled(enabled and has_model and selected)

        if enabled and not has_model:
            self.generate_docs_btn.setToolTip("Provide a model name to enable generation.")
        else:
            self.generate_docs_btn.setToolTip("")

    def _start_documentation(self) -> None:
        if not self.enable_ollama.isChecked():
            return
        chapters = self._selected_chapters()
        if not chapters:
            self.logger.warning("No chapters selected for documentation")
            return
        settings = self._gather_settings()
        request = DocumentGenerationRequest(chapters=chapters, settings=settings)
        self.logger.info(
            "Generating documentation with %s for %d chapters…",
            settings.model,
            len(chapters),
        )
        self.generate_docs_btn.setEnabled(False)
        self.chapter_list.setEnabled(False)
        self.select_all_btn.setEnabled(False)

        self._doc_thread = QThread()
        worker = DocumentationWorker(request)
        worker.moveToThread(self._doc_thread)
        self._doc_thread.started.connect(worker.run)
        worker.chapter_done.connect(self._on_chapter_documented)
        worker.chapter_failed.connect(self._on_chapter_failed)
        worker.finished.connect(lambda _: self._on_generation_finished(worker))
        self._doc_thread.start()

    def _on_chapter_documented(self, chapter_name: str, output: str) -> None:
        self.logger.info("Documentation created for %s → %s", chapter_name, output)

    def _on_chapter_failed(self, chapter_name: str, error: str) -> None:
        self.logger.error("Failed to document %s: %s", chapter_name, error)

    def _on_generation_finished(self, worker: DocumentationWorker) -> None:
        self.logger.info("Documentation generation finished")
        self.generate_docs_btn.setEnabled(True)
        self.chapter_list.setEnabled(True)
        self.select_all_btn.setEnabled(True)
        if self._doc_thread:
            self._doc_thread.quit()
            self._doc_thread.wait()
            self._doc_thread = None
        worker.deleteLater()
        self._refresh_chapter_list()
        self.generation_finished.emit()

    # Qt lifecycle -------------------------------------------------------
    def closeEvent(self, event) -> None:  # noqa: N802
        for thread in (self._split_thread, self._doc_thread):
            if thread and thread.isRunning():
                thread.quit()
                thread.wait(500)
        super().closeEvent(event)


def run() -> None:
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

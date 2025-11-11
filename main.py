# File: main.py
import sys
import logging
from pathlib import Path
from typing import Optional, Sequence

from PySide6.QtCore import Qt, QThread, QObject, Signal, QUrl
from PySide6.QtGui import QDesktopServices, QDropEvent, QDragEnterEvent
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
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QAbstractItemView,
    QSpinBox,
)

from splitter import TranscriptSplitter
from ollama_helper import (
    OllamaGenerationError,
    OllamaSettings,
    document_chapter,
)

DEFAULT_MODEL_NAME = "llama3"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TOP_P = 0.9
DEFAULT_MAX_TOKENS = 800


# Custom log handler to route logs into the QTextEdit
class QtLogHandler(logging.Handler):
    def __init__(self, widget: QTextEdit):
        super().__init__()
        self.widget = widget

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.widget.append(msg)


# Worker object to run splitting in a background thread
class SplitWorker(QObject):
    finished = Signal(int)
    error = Signal(str)
    progress = Signal(int)

    def __init__(self, splitter: TranscriptSplitter):
        super().__init__()
        self.splitter = splitter

    def run(self) -> None:
        try:
            def on_prog(current: int, total: int):
                if total:
                    self.progress.emit(int(current / total * 100))

            self.splitter.on_progress = on_prog
            count = self.splitter.split()
            self.finished.emit(count)
        except Exception as e:
            self.error.emit(str(e))


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🖋️ Markdown Transcript Splitter")
        self.resize(780, 520)
        self.current_path: Optional[Path] = None
        self.output_dir: Path = Path.cwd() / "chapters"
        self.thread: Optional[QThread] = None
        self.worker: Optional[SplitWorker] = None
        self.doc_thread: Optional[QThread] = None
        self.doc_worker: Optional[DocumentationWorker] = None

        # Layout
        container = QWidget()
        self.setCentralWidget(container)
        vbox = QVBoxLayout(container)

        # Buttons row
        row = QHBoxLayout()
        self.open_btn = QPushButton("📂 Open Markdown…")
        self.output_btn = QPushButton("📁 Select Output Dir…")
        self.split_btn = QPushButton("🚀 Split Transcript")
        self.open_folder_btn = QPushButton("📂 Open Output Folder")
        self.clear_log_btn = QPushButton("🧹 Clear Log")
        self.save_log_btn = QPushButton("💾 Save Log…")
        for btn in (
            self.open_btn,
            self.output_btn,
            self.split_btn,
            self.open_folder_btn,
            self.clear_log_btn,
            self.save_log_btn,
        ):
            row.addWidget(btn)

        self.progress = QProgressBar()
        self.progress.hide()

        self.log_area = QTextEdit(readOnly=True)
        self.log_area.setAcceptDrops(False)

        vbox.addLayout(row)
        vbox.addWidget(self.progress)

        # Ollama configuration section
        self.ollama_group = QGroupBox("LLM / Ollama")
        ollama_layout = QVBoxLayout(self.ollama_group)

        self.enable_ollama = QCheckBox("Enable documentation generation with Ollama")
        ollama_layout.addWidget(self.enable_ollama)

        form = QFormLayout()
        self.model_input = QLineEdit(DEFAULT_MODEL_NAME)
        form.addRow("Model name", self.model_input)

        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(0.0, 2.0)
        self.temperature_input.setDecimals(2)
        self.temperature_input.setSingleStep(0.05)
        self.temperature_input.setValue(DEFAULT_TEMPERATURE)
        form.addRow("Temperature", self.temperature_input)

        self.max_tokens_input = QSpinBox()
        self.max_tokens_input.setRange(1, 8192)
        self.max_tokens_input.setValue(DEFAULT_MAX_TOKENS)
        form.addRow("Max tokens", self.max_tokens_input)

        self.top_p_input = QDoubleSpinBox()
        self.top_p_input.setRange(0.0, 1.0)
        self.top_p_input.setDecimals(2)
        self.top_p_input.setSingleStep(0.05)
        self.top_p_input.setValue(DEFAULT_TOP_P)
        form.addRow("Top_p", self.top_p_input)

        ollama_layout.addLayout(form)

        self.chapter_list = QListWidget()
        self.chapter_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.chapter_list.setMinimumHeight(140)
        ollama_layout.addWidget(QLabel("Chapters ready for documentation:"))
        ollama_layout.addWidget(self.chapter_list)

        doc_controls = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        doc_controls.addWidget(self.select_all_btn)
        self.generate_docs_btn = QPushButton("Generate Documentation for Chapters")
        doc_controls.addWidget(self.generate_docs_btn)
        ollama_layout.addLayout(doc_controls)

        vbox.addWidget(self.ollama_group)
        vbox.addWidget(self.log_area)

        # Logger setup
        self.logger = logging.getLogger("transcript_splitter")
        self.logger.setLevel(logging.DEBUG)
        handler = QtLogHandler(self.log_area)
        handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        )
        self.logger.addHandler(handler)

        # Connections
        self.open_btn.clicked.connect(self.open_file)
        self.output_btn.clicked.connect(self.select_output)
        self.split_btn.clicked.connect(self.start_split)
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        self.clear_log_btn.clicked.connect(self.log_area.clear)
        self.save_log_btn.clicked.connect(self.save_log)
        self.enable_ollama.stateChanged.connect(self.update_doc_controls)
        self.model_input.textChanged.connect(self.update_doc_controls)
        self.select_all_btn.clicked.connect(self.select_all_chapters)
        self.generate_docs_btn.clicked.connect(self.start_documentation)

        self.setAcceptDrops(True)
        self.update_doc_controls()
        self.refresh_chapter_list()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        urls = event.mimeData().urls()
        if urls:
            path = Path(urls[0].toLocalFile())
            if path.suffix.lower() == ".md":
                self.load_markdown(path)

    def open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "🔍 Select Transcript Markdown", str(Path.cwd()), "Markdown Files (*.md)"
        )
        if path:
            self.load_markdown(Path(path))

    def load_markdown(self, path: Path) -> None:
        self.current_path = path
        self.logger.info(f"📥 Loaded input file: {path}")

    def select_output(self) -> None:
        dirpath = QFileDialog.getExistingDirectory(
            self, "🔍 Select Output Directory", str(self.output_dir)
        )
        if dirpath:
            self.output_dir = Path(dirpath)
            self.logger.info(f"📂 Output directory set to: {self.output_dir}")
            self.refresh_chapter_list()

    def start_split(self) -> None:
        if not self.current_path:
            self.logger.error("❌ No input file selected.")
            return
        self.logger.info("🚀 Starting split…")
        for btn in (self.open_btn, self.output_btn, self.split_btn):
            btn.setEnabled(False)
        self.progress.setValue(0)
        self.progress.show()

        splitter = TranscriptSplitter(self.current_path, self.output_dir)
        self.thread = QThread()
        self.worker = SplitWorker(splitter)
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_split_complete)
        self.worker.error.connect(self.on_split_error)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def on_split_complete(self, count: int) -> None:
        self.logger.info(f"✅ Split complete: {count} chapters generated.")
        # Log each created file
        for fpath in sorted(self.output_dir.glob("*.md")):
            self.logger.info(f"📄 Created file: {fpath.name}")
        self.progress.hide()
        for btn in (self.open_btn, self.output_btn, self.split_btn):
            btn.setEnabled(True)
        if self.thread:
            self.thread.quit()
            self.thread.wait()
            self.thread = None
            self.worker = None
        self.refresh_chapter_list()

    def on_split_error(self, msg: str) -> None:
        self.logger.error(f"❌ Error during split: {msg}")
        self.progress.hide()
        for btn in (self.open_btn, self.output_btn, self.split_btn):
            btn.setEnabled(True)
        if self.thread:
            self.thread.quit()
            self.thread.wait()
            self.thread = None
            self.worker = None

    def open_output_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.output_dir)))

    def save_log(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "💾 Save Log As…", "splitter_log.txt", "Text Files (*.txt)"
        )
        if path:
            Path(path).write_text(self.log_area.toPlainText(), encoding="utf-8")
            self.logger.info(f"💾 Log saved to: {path}")

    # --- Documentation utilities -------------------------------------------------
    def refresh_chapter_list(self) -> None:
        self.chapter_list.clear()
        if not self.output_dir.exists():
            self.update_doc_controls()
            return
        chapter_paths = sorted(self.output_dir.glob("*.md"))
        for chapter in chapter_paths:
            if chapter.name.endswith(".docs.md"):
                continue
            item = QListWidgetItem(chapter.name)
            item.setData(Qt.UserRole, chapter)
            self.chapter_list.addItem(item)
        self.update_doc_controls()

    def select_all_chapters(self) -> None:
        for index in range(self.chapter_list.count()):
            self.chapter_list.item(index).setSelected(True)
        self.update_doc_controls()

    def collect_selected_chapters(self) -> list[Path]:
        chapters: list[Path] = []
        for item in self.chapter_list.selectedItems():
            data = item.data(Qt.UserRole)
            if isinstance(data, Path):
                chapters.append(data)
        return chapters

    def collect_settings(self) -> OllamaSettings:
        return OllamaSettings(
            model=self.model_input.text().strip(),
            temperature=float(self.temperature_input.value()),
            max_tokens=int(self.max_tokens_input.value()),
            top_p=float(self.top_p_input.value()),
        )

    def update_doc_controls(self) -> None:
        enabled = self.enable_ollama.isChecked()
        has_model = bool(self.model_input.text().strip())
        has_chapters = self.chapter_list.count() > 0
        selected = len(self.collect_selected_chapters()) > 0

        self.ollama_group.setEnabled(True)
        self.model_input.setEnabled(enabled)
        self.temperature_input.setEnabled(enabled)
        self.max_tokens_input.setEnabled(enabled)
        self.top_p_input.setEnabled(enabled)
        self.chapter_list.setEnabled(enabled)
        self.select_all_btn.setEnabled(enabled and has_chapters)

        self.generate_docs_btn.setEnabled(enabled and has_model and selected)
        if enabled and not has_model:
            self.generate_docs_btn.setToolTip("Provide a model name to generate documentation.")
        else:
            self.generate_docs_btn.setToolTip("")

    def start_documentation(self) -> None:
        if not self.enable_ollama.isChecked():
            return
        chapters = self.collect_selected_chapters()
        if not chapters:
            self.logger.warning("⚠️ No chapters selected for documentation.")
            return
        settings = self.collect_settings()
        if not settings.model:
            self.logger.error("❌ No model configured for Ollama generation.")
            return

        self.logger.info(
            "🧠 Generating documentation with %s for %d chapters…",
            settings.model,
            len(chapters),
        )
        self.generate_docs_btn.setEnabled(False)
        self.chapter_list.setEnabled(False)
        self.select_all_btn.setEnabled(False)

        self.doc_thread = QThread()
        self.doc_worker = DocumentationWorker(chapters, settings)
        self.doc_worker.moveToThread(self.doc_thread)
        self.doc_thread.started.connect(self.doc_worker.run)
        self.doc_worker.finished.connect(self.on_documentation_finished)
        self.doc_worker.chapter_done.connect(self.on_chapter_documented)
        self.doc_worker.chapter_failed.connect(self.on_chapter_failed)
        self.doc_thread.start()

    def on_documentation_finished(self) -> None:
        self.logger.info("✅ Documentation generation finished.")
        if self.doc_thread:
            self.doc_thread.quit()
            self.doc_thread.wait()
            self.doc_thread = None
            self.doc_worker = None
        self.refresh_chapter_list()
        self.chapter_list.setEnabled(self.enable_ollama.isChecked())
        self.select_all_btn.setEnabled(self.enable_ollama.isChecked())

    def on_chapter_documented(self, chapter_name: str, output_path: str) -> None:
        self.logger.info(f"📝 Documentation created for {chapter_name}: {output_path}")

    def on_chapter_failed(self, chapter_name: str, error: str) -> None:
        self.logger.error(f"❌ Failed to document {chapter_name}: {error}")


    # -------------------------------------------------------------------------
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

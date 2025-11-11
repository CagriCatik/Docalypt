"""Main PySide6 GUI for Docalypt."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QDesktopServices, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
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
    QTabWidget,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QAbstractItemView,
    QMessageBox,
)

from ..documentation import (
    DOCUMENTATION_SUBDIR,
    DocumentGenerationRequest,
    DocumentGenerationResult,
    LLMSettings,
    collect_chapter_files,
)
from ..llm import (
    DEFAULT_ANTHROPIC_ENDPOINT,
    DEFAULT_ANTHROPIC_VERSION,
    DEFAULT_OLLAMA_ENDPOINT,
    DEFAULT_OPENAI_ENDPOINT,
    PROMPT_TEMPLATE,
    settings_from_env,
)
from ..splitting import TranscriptSplitter
from .common import DocumentationWorker, ModelListWorker, QtLogHandler, SplitWorker

DEFAULT_MODEL = "llama3"
DOCS_SUBDIR = DOCUMENTATION_SUBDIR
PROVIDER_OPTIONS = [
    ("Local Ollama", "ollama"),
    ("OpenAI compatible", "openai"),
    ("Anthropic Claude", "anthropic"),
]


class MainWindow(QMainWindow):
    generation_finished = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Docalypt • Transcript Splitter & Doc Generator")
        self.resize(860, 540)
        self.setAcceptDrops(True)

        self.logger = logging.getLogger("docalypt.gui")
        self.logger.setLevel(logging.INFO)

        self._default_llm_settings = settings_from_env()
        self._input_path: Optional[Path] = None
        self._output_dir: Path = Path.cwd() / "chapters"
        self._split_thread: Optional[QThread] = None
        self._split_worker: Optional[SplitWorker] = None
        self._doc_thread: Optional[QThread] = None
        self._doc_worker: Optional[DocumentationWorker] = None
        self._model_thread: Optional[QThread] = None
        self._model_worker: Optional[ModelListWorker] = None
        self._available_models: list[str] = []
        self._pending_model_provider: Optional[str] = None

        self._build_ui()
        self._apply_default_settings()
        self._connect_signals()
        self._refresh_chapter_list()
        self._update_doc_controls()
        self._refresh_models()

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

        self.ollama_group = QGroupBox("LLM Provider")
        ollama_layout = QVBoxLayout(self.ollama_group)

        self.enable_ollama = QCheckBox(
            "Enable documentation generation with an LLM provider"
        )
        ollama_layout.addWidget(self.enable_ollama)

        self.ollama_tabs = QTabWidget()
        ollama_layout.addWidget(self.ollama_tabs)

        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        form = QFormLayout()

        self.provider_combo = QComboBox()
        for label, value in PROVIDER_OPTIONS:
            self.provider_combo.addItem(label, value)
        form.addRow("Provider", self.provider_combo)

        self.endpoint_edit = QLineEdit()
        self.endpoint_edit.setPlaceholderText(DEFAULT_OLLAMA_ENDPOINT)
        form.addRow("Endpoint", self.endpoint_edit)

        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.setInsertPolicy(QComboBox.NoInsert)
        self.model_combo.setPlaceholderText("Select or type a model…")
        self.model_combo.setCurrentText(DEFAULT_MODEL)
        self.refresh_models_btn = QPushButton("Refresh models")
        model_row = QHBoxLayout()
        model_row.addWidget(self.model_combo, stretch=1)
        model_row.addWidget(self.refresh_models_btn)
        model_widget = QWidget()
        model_widget.setLayout(model_row)
        form.addRow("Model", model_widget)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        self.api_key_edit.setPlaceholderText("API key required for hosted providers")
        self.api_key_row = QWidget()
        api_layout = QHBoxLayout(self.api_key_row)
        api_layout.setContentsMargins(0, 0, 0, 0)
        api_layout.addWidget(self.api_key_edit)
        form.addRow("API key", self.api_key_row)

        self.version_edit = QLineEdit()
        self.version_edit.setPlaceholderText(DEFAULT_ANTHROPIC_VERSION)
        self.version_row = QWidget()
        version_layout = QHBoxLayout(self.version_row)
        version_layout.setContentsMargins(0, 0, 0, 0)
        version_layout.addWidget(self.version_edit)
        form.addRow("API version", self.version_row)

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

        self.presence_penalty_spin = QDoubleSpinBox()
        self.presence_penalty_spin.setRange(-2.0, 2.0)
        self.presence_penalty_spin.setDecimals(2)
        self.presence_penalty_spin.setSingleStep(0.1)
        self.presence_penalty_spin.setValue(0.0)
        form.addRow("Presence penalty", self.presence_penalty_spin)

        self.frequency_penalty_spin = QDoubleSpinBox()
        self.frequency_penalty_spin.setRange(-2.0, 2.0)
        self.frequency_penalty_spin.setDecimals(2)
        self.frequency_penalty_spin.setSingleStep(0.1)
        self.frequency_penalty_spin.setValue(0.0)
        form.addRow("Frequency penalty", self.frequency_penalty_spin)

        self.repeat_penalty_spin = QDoubleSpinBox()
        self.repeat_penalty_spin.setRange(0.0, 2.0)
        self.repeat_penalty_spin.setDecimals(2)
        self.repeat_penalty_spin.setSingleStep(0.1)
        self.repeat_penalty_spin.setValue(1.0)
        form.addRow("Repeat penalty", self.repeat_penalty_spin)

        self.top_k_spin = QSpinBox()
        self.top_k_spin.setRange(1, 1000)
        self.top_k_spin.setValue(40)
        form.addRow("Top_k", self.top_k_spin)

        settings_layout.addLayout(form)
        settings_layout.addStretch(1)

        prompt_tab = QWidget()
        prompt_layout = QVBoxLayout(prompt_tab)
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setAcceptRichText(False)
        self.prompt_edit.setPlainText(PROMPT_TEMPLATE)
        prompt_layout.addWidget(QLabel("Prompt template"))
        prompt_layout.addWidget(self.prompt_edit, stretch=1)
        self.reset_prompt_btn = QPushButton("Reset to default prompt")
        prompt_layout.addWidget(self.reset_prompt_btn, alignment=Qt.AlignRight)

        self.ollama_tabs.addTab(settings_tab, "Model & Parameters")
        self.ollama_tabs.addTab(prompt_tab, "Prompt Ingestion")

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

    def _apply_default_settings(self) -> None:
        settings = self._default_llm_settings
        provider = (settings.provider or "ollama").strip().lower()
        valid_providers = {value for _, value in PROVIDER_OPTIONS}
        if provider not in valid_providers:
            provider = "ollama"
        index = self.provider_combo.findData(provider)
        if index >= 0:
            self.provider_combo.setCurrentIndex(index)
        else:
            self.provider_combo.setCurrentIndex(0)

        if settings.model:
            self.model_combo.setCurrentText(settings.model)
        else:
            self.model_combo.setCurrentText(DEFAULT_MODEL)

        if settings.endpoint:
            self.endpoint_edit.setText(settings.endpoint)
        else:
            self.endpoint_edit.setText("")

        if settings.api_key:
            self.api_key_edit.setText(settings.api_key)
        else:
            self.api_key_edit.clear()

        if settings.anthropic_version:
            self.version_edit.setText(settings.anthropic_version)
        else:
            self.version_edit.setText(DEFAULT_ANTHROPIC_VERSION)

        self._apply_provider_fields()

    def _apply_provider_fields(self) -> None:
        provider = self._current_provider()
        endpoint_placeholder = self._default_endpoint_for(provider)
        self.endpoint_edit.setPlaceholderText(endpoint_placeholder)

        requires_key = self._provider_requires_key(provider)
        is_anthropic = provider == "anthropic"

        self.api_key_row.setVisible(requires_key)
        self.version_row.setVisible(is_anthropic)

        if is_anthropic and not self.version_edit.text().strip():
            self.version_edit.setText(DEFAULT_ANTHROPIC_VERSION)

    def _current_provider(self) -> str:
        data = self.provider_combo.currentData()
        if isinstance(data, str):
            return data
        return "ollama"

    def _default_endpoint_for(self, provider: str) -> str:
        if provider == "openai":
            return DEFAULT_OPENAI_ENDPOINT
        if provider == "anthropic":
            return DEFAULT_ANTHROPIC_ENDPOINT
        return DEFAULT_OLLAMA_ENDPOINT

    @staticmethod
    def _provider_requires_key(provider: str) -> bool:
        return provider in {"openai", "anthropic"}

    def _provider_label(self, provider: str) -> str:
        for label, value in PROVIDER_OPTIONS:
            if value == provider:
                return label
        return provider.capitalize()

    def _connect_signals(self) -> None:
        self.open_btn.clicked.connect(self._open_file)
        self.output_btn.clicked.connect(self._select_output)
        self.split_btn.clicked.connect(self._start_split)
        self.open_folder_btn.clicked.connect(self._reveal_output)
        self.clear_log_btn.clicked.connect(self.log_area.clear)
        self.save_log_btn.clicked.connect(self._save_log)
        self.enable_ollama.stateChanged.connect(self._update_doc_controls)
        self.provider_combo.currentIndexChanged.connect(self._on_provider_changed)
        self.model_combo.currentTextChanged.connect(self._update_doc_controls)
        self.chapter_list.itemSelectionChanged.connect(self._update_doc_controls)
        self.select_all_btn.clicked.connect(self._select_all)
        self.generate_docs_btn.clicked.connect(self._start_documentation)
        self.refresh_models_btn.clicked.connect(self._refresh_models)
        self.reset_prompt_btn.clicked.connect(self._reset_prompt)

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

        if self._split_thread and self._split_thread.isRunning():
            self.logger.warning("A split operation is already running")
            return

        splitter = TranscriptSplitter(self._input_path, self._output_dir)
        thread = QThread(self)
        worker = SplitWorker(splitter)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.progress.connect(self.progress.setValue)
        worker.finished.connect(self._on_split_finished)
        worker.error.connect(self._on_split_error)
        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        thread.finished.connect(self._cleanup_split_thread)

        self._split_thread = thread
        self._split_worker = worker
        thread.start()

    def _on_split_finished(self, count: int) -> None:
        self.logger.info("Split complete: %d chapters", count)
        self.progress.hide()
        self.split_btn.setEnabled(True)
        self._refresh_chapter_list()

    def _on_split_error(self, message: str) -> None:
        self.logger.error("Split failed: %s", message)
        self.progress.hide()
        self.split_btn.setEnabled(True)

    def _cleanup_split_thread(self) -> None:
        if self._split_worker:
            self._split_worker.deleteLater()
            self._split_worker = None
        if self._split_thread:
            self._split_thread.deleteLater()
            self._split_thread = None
        self._update_doc_controls()

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

    def _reset_prompt(self) -> None:
        self.prompt_edit.setPlainText(PROMPT_TEMPLATE)
        self.logger.info("Prompt template reset to default")

    def _on_provider_changed(self) -> None:
        self._apply_provider_fields()
        provider = self._current_provider()
        if provider != "ollama" and self._available_models:
            self._available_models = []
            self._apply_model_choices([])
        self._update_doc_controls()

    def _refresh_models(self) -> None:
        if self._model_thread and self._model_thread.isRunning():
            return
        provider = self._current_provider()
        if provider != "ollama":
            self.logger.info(
                "Model listing is only available for local Ollama providers."
            )
            return
        self.logger.info("Refreshing Ollama models…")
        self.refresh_models_btn.setEnabled(False)
        self.refresh_models_btn.setText("Refreshing…")

        self._pending_model_provider = provider
        worker = ModelListWorker(self._gather_settings(require_model=False))
        thread = QThread(self)
        self._model_worker = worker
        self._model_thread = thread
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(self._handle_models_loaded)
        worker.failed.connect(self._handle_models_failed)
        worker.finished.connect(thread.quit)
        worker.failed.connect(thread.quit)
        thread.finished.connect(self._finalize_model_refresh)
        thread.start()

    def _handle_models_loaded(self, models: list[str]) -> None:
        self._on_models_loaded(models)

    def _handle_models_failed(self, message: str) -> None:
        self._on_models_failed(message)

    def _on_models_loaded(self, models: list[str]) -> None:
        self._available_models = models
        provider = self._pending_model_provider or "ollama"
        label = self._provider_label(provider)
        if models:
            self.logger.info("Discovered %d model(s) from %s", len(models), label)
        else:
            self.logger.warning("No models were reported by %s", label)
        self._apply_model_choices(models)

    def _on_models_failed(self, message: str) -> None:
        provider = self._pending_model_provider or "ollama"
        label = self._provider_label(provider)
        self.logger.error("Failed to query models from %s: %s", label, message)

    def _apply_model_choices(self, models: list[str]) -> None:
        current_text = self.model_combo.currentText().strip()
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        if models:
            self.model_combo.addItems(models)
        if current_text:
            index = self.model_combo.findText(current_text)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)
            else:
                self.model_combo.setEditText(current_text)
        elif models:
            self.model_combo.setCurrentIndex(0)
        else:
            self.model_combo.setEditText(DEFAULT_MODEL)
        self.model_combo.blockSignals(False)
        self._update_doc_controls()

    def _finalize_model_refresh(self) -> None:
        if self._model_worker:
            self._model_worker.deleteLater()
            self._model_worker = None
        if self._model_thread:
            self._model_thread.deleteLater()
            self._model_thread = None
        self.refresh_models_btn.setText("Refresh models")
        self.refresh_models_btn.setEnabled(True)
        self._pending_model_provider = None
        self._update_doc_controls()

    def _gather_settings(self, require_model: bool = True) -> LLMSettings:
        provider = self._current_provider()
        model = self.model_combo.currentText().strip()
        if not model and not require_model:
            model = ""
        endpoint = self.endpoint_edit.text().strip() or None
        api_key = self.api_key_edit.text().strip() or None
        version = self.version_edit.text().strip() or None
        settings = LLMSettings(
            provider=provider,
            model=model,
            temperature=float(self.temperature_spin.value()),
            top_p=float(self.top_p_spin.value()),
            max_tokens=int(self.max_tokens_spin.value()),
            presence_penalty=float(self.presence_penalty_spin.value()),
            frequency_penalty=float(self.frequency_penalty_spin.value()),
            repeat_penalty=float(self.repeat_penalty_spin.value()),
            top_k=int(self.top_k_spin.value()),
            endpoint=endpoint,
            api_key=api_key,
            anthropic_version=version or None,
        )
        if provider == "anthropic" and not settings.anthropic_version:
            settings.anthropic_version = DEFAULT_ANTHROPIC_VERSION
        return settings

    def _update_doc_controls(self) -> None:
        enabled = self.enable_ollama.isChecked()
        provider = self._current_provider()
        requires_key = self._provider_requires_key(provider)
        is_anthropic = provider == "anthropic"
        is_ollama = provider == "ollama"
        self._apply_provider_fields()

        has_model = bool(self.model_combo.currentText().strip())
        selected = bool(self._selected_chapters())
        has_chapters = self.chapter_list.count() > 0
        has_key = bool(self.api_key_edit.text().strip()) if requires_key else True

        for widget in (
            self.provider_combo,
            self.endpoint_edit,
            self.model_combo,
            self.temperature_spin,
            self.top_p_spin,
            self.max_tokens_spin,
            self.presence_penalty_spin,
            self.frequency_penalty_spin,
            self.repeat_penalty_spin,
            self.top_k_spin,
            self.chapter_list,
            self.select_all_btn,
            self.prompt_edit,
            self.reset_prompt_btn,
            self.ollama_tabs,
        ):
            widget.setEnabled(enabled)

        self.api_key_edit.setEnabled(enabled and requires_key)
        self.version_edit.setEnabled(enabled and is_anthropic)

        self.refresh_models_btn.setVisible(is_ollama)
        self.refresh_models_btn.setEnabled(enabled and is_ollama)
        if not is_ollama:
            self.refresh_models_btn.setToolTip(
                "Model discovery is only available for local Ollama instances."
            )
        else:
            self.refresh_models_btn.setToolTip("")

        self.select_all_btn.setEnabled(enabled and has_chapters)
        ready = enabled and has_model and selected and has_key
        self.generate_docs_btn.setEnabled(ready)

        if enabled and not has_model:
            self.generate_docs_btn.setToolTip(
                "Provide a model name to enable generation."
            )
        elif enabled and not has_key:
            self.generate_docs_btn.setToolTip(
                "Provide an API key for the selected provider to enable generation."
            )
        else:
            self.generate_docs_btn.setToolTip("")

        if self._model_thread and self._model_thread.isRunning():
            self.refresh_models_btn.setEnabled(False)

    def _start_documentation(self) -> None:
        if not self.enable_ollama.isChecked():
            return
        chapters = self._selected_chapters()
        if not chapters:
            self.logger.warning("No chapters selected for documentation")
            return
        settings = self._gather_settings()
        prompt_template = self.prompt_edit.toPlainText().strip() or PROMPT_TEMPLATE
        request = DocumentGenerationRequest(
            chapters=chapters,
            settings=settings,
            prompt_template=prompt_template,
            destination_dirname=DOCS_SUBDIR,
        )
        self.logger.info(
            "Generating documentation with %s (%s) for %d chapters…",
            settings.model,
            self._provider_label(settings.provider),
            len(chapters),
        )
        self.generate_docs_btn.setEnabled(False)
        self.chapter_list.setEnabled(False)
        self.select_all_btn.setEnabled(False)

        if self._doc_thread and self._doc_thread.isRunning():
            self.logger.warning("Documentation is already running")
            return

        thread = QThread(self)
        worker = DocumentationWorker(request)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.chapter_done.connect(self._on_chapter_documented)
        worker.chapter_failed.connect(self._on_chapter_failed)
        worker.finished.connect(self._on_generation_finished)
        worker.finished.connect(thread.quit)
        thread.finished.connect(self._cleanup_doc_thread)

        self._doc_thread = thread
        self._doc_worker = worker
        thread.start()

    def _on_chapter_documented(self, chapter_name: str, output: str) -> None:
        self.logger.info("Documentation created for %s → %s", chapter_name, output)

    def _on_chapter_failed(self, chapter_name: str, error: str) -> None:
        self.logger.error("Failed to document %s: %s", chapter_name, error)

    def _on_generation_finished(self, result: DocumentGenerationResult) -> None:
        self.logger.info(
            "Documentation generation finished (%d succeeded, %d failed)",
            len(result.written),
            len(result.failures),
        )
        if result.written:
            target_dir = self._output_dir / DOCS_SUBDIR
            self.logger.info("Documentation stored in %s", target_dir)
        self.generate_docs_btn.setEnabled(True)
        self.chapter_list.setEnabled(True)
        self.select_all_btn.setEnabled(True)
        self._refresh_chapter_list()
        self.generation_finished.emit()

    def _cleanup_doc_thread(self) -> None:
        if self._doc_worker:
            self._doc_worker.deleteLater()
            self._doc_worker = None
        if self._doc_thread:
            self._doc_thread.deleteLater()
            self._doc_thread = None
        self._update_doc_controls()

    # Qt lifecycle -------------------------------------------------------
    def closeEvent(self, event) -> None:  # noqa: N802
        for thread in (self._split_thread, self._doc_thread, self._model_thread):
            if thread and thread.isRunning():
                thread.quit()
                thread.wait(500)
        super().closeEvent(event)


def run() -> None:
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

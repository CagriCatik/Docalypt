# File: main.py
import sys
import logging
from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QFileDialog, QProgressBar
)
from PySide6.QtCore import Qt, QThread, QObject, Signal
from PySide6.QtGui import QDesktopServices, QDropEvent, QDragEnterEvent
from PySide6.QtCore import QUrl
from splitter import TranscriptSplitter

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
                self.progress.emit(int(current / total * 100))
            self.splitter.on_progress = on_prog
            count = self.splitter.split()
            self.finished.emit(count)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🖋️ Markdown Transcript Splitter")
        self.resize(600, 200)
        self.current_path: Optional[Path] = None
        self.output_dir: Path = Path.cwd() / "chapters"

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
        for btn in (self.open_btn, self.output_btn, self.split_btn,
                    self.open_folder_btn, self.clear_log_btn, self.save_log_btn):
            row.addWidget(btn)

        self.progress = QProgressBar()
        self.progress.hide()

        self.log_area = QTextEdit(readOnly=True)
        self.log_area.setAcceptDrops(False)

        vbox.addLayout(row)
        vbox.addWidget(self.progress)
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

        self.setAcceptDrops(True)

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
        for fpath in self.output_dir.glob("*.md"):
            self.logger.info(f"📄 Created file: {fpath.name}")
        self.progress.hide()
        for btn in (self.open_btn, self.output_btn, self.split_btn):
            btn.setEnabled(True)
        self.thread.quit()

    def on_split_error(self, msg: str) -> None:
        self.logger.error(f"❌ Error during split: {msg}")
        self.progress.hide()
        for btn in (self.open_btn, self.output_btn, self.split_btn):
            btn.setEnabled(True)
        self.thread.quit()

    def open_output_folder(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.output_dir)))

    def save_log(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "💾 Save Log As…", "splitter_log.txt", "Text Files (*.txt)"
        )
        if path:
            Path(path).write_text(self.log_area.toPlainText(), encoding='utf-8')
            self.logger.info(f"💾 Log saved to: {path}")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
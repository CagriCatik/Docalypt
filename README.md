# Docalypt

A lightweight, flexible tool for splitting Markdown-formatted transcripts into timestamped chapter files. Supports both GUI (PySide6) and CLI interfaces, plugin hooks, custom markers, and optional HTML export.

---

## Features

- **Split Markdown by timestamps**: Detect markers like `(HH:MM:SS)` or custom regex patterns.
- **GUI & CLI**:
  - **GUI**: Full-featured `main.py` with drag-&-drop, progress bar, log pane, and compact version `compact_gui.py`.
  - **CLI**: `cli.py` built with [Click](https://click.palletsprojects.com/).
- **Configurable**: Load defaults from `~/.config/markdown_splitter/config.toml`:
  ```toml
  marker_regex = "\((\d{1,2}:\d{2}(?::\d{2})?)\)"
  output_dir   = "/home/user/chapters"
  ```
- **Plugin hooks**:
  - **pre-split**: modify the body text before splitting.
  - **post-split**: act on each generated file (e.g. watermark, log).
- **HTML Export**: `--html` flag to produce a simple `index.html` aggregating all chapters.
- **Type-checked**: Uses type hints and `pathlib` for clarity and safety.

## Installation (with Poetry)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/markdown-transcript-splitter.git
   cd markdown-transcript-splitter
   ```

2. **Install dependencies** via Poetry:
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

> **Requirements**: Python 3.8+, Poetry, PySide6, toml, click

## Configuration

Create or edit `~/.config/markdown_splitter/config.toml` to override defaults:

```toml
marker_regex = "\[(\d{2}:\d{2}:\d{2})\]"
output_dir   = "/path/to/output"
html_template = null  # (future: supply custom HTML template)
```

## Usage

### CLI

```bash
# Basic split:
python cli.py transcript.md

# Specify output directory:
python cli.py transcript.md -o ./output

# Custom split marker:
python cli.py transcript.md -m '\[(\d{1,2}:\d{2})\]'

# Also generate HTML index:
python cli.py transcript.md --html

# Verbose debug logging:
python cli.py transcript.md -v
```

### Full GUI

```bash
python main.py
```

- Drag & drop `.md` onto the window or use **📂 Open Markdown…**
- Choose output folder, then **🚀 Split Transcript**

### Compact GUI

```bash
python compact_gui.py
```

- Browse for a file, then click **Split**
- Minimal pop-up dialogs indicate success or errors

## Extending with Hooks

You can pass your own functions to `TranscriptSplitter`:

```python
from splitter import TranscriptSplitter

def uppercase_body(body: str) -> str:
    return body.upper()

def log_file(path):
    print(f"Generated {path}")

splitter = TranscriptSplitter(
    input_path=Path('transcript.md'),
    output_dir=Path('./chapters'),
    pre_split_hooks=[uppercase_body],
    post_split_hooks=[log_file]
)
splitter.split(export_html=True)
```

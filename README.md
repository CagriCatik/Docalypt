# Docalypt

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![UI-PySide6](https://img.shields.io/badge/UI-PySide6-brightgreen)](https://doc.qt.io/qtforpython-6/)
[![LLM-Ollama](https://img.shields.io/badge/LLM-Ollama-orange)](https://ollama.com/)
[![Interface](https://img.shields.io/badge/interface-CLI%20%7C%20GUI%20%7C%20Streamlit-informational)](#running-docalypt)

Docalypt is a transcript productivity toolkit. It parses long-form Markdown
transcripts into clean chapter files, renders optional HTML summaries, and can
ask a local Ollama model to generate documentation for each chapter. All user
interfaces—CLI, PySide6 desktop, and Streamlit web—share the same application
services so behaviour remains consistent everywhere.

---

## Features

- **Layered architecture** – domain parsing, application use-cases, and
  infrastructure adapters are cleanly separated for easier testing and future
  extension.
- **Multiple front-ends** – use the CLI for automation, the PySide desktop UI for
  power-user workflows, or the Streamlit app for quick web-based reviews.
- **Pluggable persistence & prompts** – filesystem repository renders chapters
  and HTML via Jinja2 templates while prompt templates are user configurable.
- **Ollama integration** – list local models, tune generation settings, and
  stream results into any interface.
- **Sample data** – example transcripts, prompts, and generated chapters live
  under `examples/` to keep the repository lean and reproducible.

## Project structure

```
.
├── docalypt/
│   ├── application/            # Use-cases coordinating domain & infrastructure
│   ├── domain/                 # Pure models and transcript parser
│   ├── infrastructure/
│   │   ├── config/             # TOML configuration loader
│   │   ├── llm/                # Ollama HTTP gateway
│   │   └── storage/            # Filesystem repositories & templates
│   ├── interfaces/
│   │   ├── cli/                # Click-based CLI wiring
│   │   ├── gui/                # PySide6 windows and workers
│   │   └── streamlit/          # Streamlit view logic
│   ├── documentation.py        # Compatibility façade around new services
│   ├── ollama.py               # Backwards-compatible Ollama exports
│   └── splitting.py            # Compatibility façade for TranscriptSplitter
├── cli.py                      # CLI entry point (delegates to interfaces.cli)
├── main.py                     # PySide6 launcher
├── streamlit_app.py            # Streamlit entry point
├── examples/                   # Sample transcripts, prompts, and chapters
└── docs/                       # Architecture notes and design docs
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for a diagram of the clean
architecture and extension guidance.

## Installation

1. **Clone and create a virtual environment**

   ```bash
   git clone https://github.com/CagriCatik/Docalypt.git
   cd Docalypt
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama (optional)**

   Download from [ollama.com](https://ollama.com/), run the service, and pull a
   model (for example `ollama pull llama3`). The documentation workflows will
   skip Ollama integration automatically if the service is unavailable.

## Running Docalypt

### CLI

Split a transcript and (optionally) render an HTML index:

```bash
python cli.py split examples/transcripts/esp32_iot_4_layer_pcb.md --output-dir ./output --html
```

Generate documentation for an existing chapter directory:

```bash
python cli.py docs ./output --model llama3 --temperature 0.3
```

### PySide desktop GUI

```bash
python main.py
```

1. Select or drag a transcript into the window.
2. Pick an output directory (defaults to `examples/chapters`).
3. Click **Split Transcript** to generate chapter Markdown files.
4. Enable the Ollama panel to configure generation parameters and create
   documentation.

### Streamlit web app

```bash
streamlit run streamlit_app.py
```

The Streamlit UI provides two tabs:

1. **Split Transcript** – upload a Markdown transcript, choose an output
   directory, and optionally render an HTML index. Results are stored on disk and
   listed in the UI.
2. **Generate Documentation** – select chapters, adjust Ollama settings, and
   stream documentation output. Results reuse the same file layout as the CLI and
   desktop app.

## Configuration

Runtime settings live in `~/.config/docalypt/config.toml`:

```toml
marker_regex = "\((\d{1,2}:\d{2}(?::\d{2})?)\)"
output_dir = "~/docalypt/chapters"
html_template = "~/docalypt/templates/index.html"
```

- `marker_regex` – regex used to detect timestamp markers.
- `output_dir` – default directory for generated chapters.
- `html_template` – optional path to a custom Jinja2 template used for the HTML
  index.

If no config file exists, sensible defaults are applied automatically.

## Sample workflow

Example assets in `examples/` match the repository’s default settings:

1. Split the included transcript with the CLI:

   ```bash
   python cli.py split examples/transcripts/esp32_iot_4_layer_pcb.md --output-dir examples/chapters --html
   ```

2. Launch the Streamlit app and open the **Generate Documentation** tab to select
   from the same `examples/chapters` directory.

3. Use the PySide GUI to explore the same files—the chapter list and generated
   documents remain in sync because all front-ends share the filesystem
   repository.

## Extending & contributing

- New persistence backends should implement the `ChapterRepository` protocol and
  live under `docalypt/infrastructure/storage/`.
- Alternative LLM providers should implement `DocumentationGateway` under
  `docalypt/infrastructure/llm/` and be wired into
  `GenerateDocumentationUseCase`.
- Front-end additions belong under `docalypt/interfaces/` and should depend only
  on application services.
- Run `ruff`/`black`/`pytest` (or your preferred equivalents) before submitting
  changes; add unit tests for new business logic where practical.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for
details.

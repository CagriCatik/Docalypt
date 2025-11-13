<img src="./assets/logo.png" alt="Docalypt Logo" width="200"/>

[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![UI-PySide6](https://img.shields.io/badge/UI-PySide6-brightgreen)](https://doc.qt.io/qtforpython-6/)
[![LLM-Ollama](https://img.shields.io/badge/LLM-Ollama-orange)](https://ollama.com/)
[![Interface](https://img.shields.io/badge/interface-CLI%20%7C%20GUI-informational)](#running-docalypt)

Docalypt automates the conversion of long-form Markdown transcripts into clean, timestamped chapter files. It can optionally generate AI-enhanced documentation for each chapter using local Ollama models or hosted LLM providers. Both the GUI and CLI use the same underlying pipeline to ensure consistent behavior across interfaces.

---

<div style="text-align: center;">
  <img src="./assets/screenshot.png" alt="Docalypt Screenshot" width="600"/>
</div>

---

## Key features

* **Consistent splitting engine**  
  Produces deterministic chapter boundaries and a stable on-disk structure compatible with earlier versions.

* **Responsive PySide6 desktop app**  
  Drag and drop transcripts, track progress, and generate documentation without blocking the UI.

* **Integrated Ollama controls**  
  Inspect installed models, tune generation parameters, customize prompts, and run documentation jobs.

* **Multiple LLM providers**  
  Switch between local Ollama and hosted services (OpenAI, Anthropic) using a simple `.env` configuration.

* **Clear output structure**  
  AI-generated docs are stored under a dedicated `documentation/` subdirectory next to the chapter files.

* **Single shared codebase**  
  The GUI and CLI reuse the same configuration, splitting logic, and LLM utilities.

## Repository structure

```bash
├── Docalypt/
│   ├── documentation.py     # Documentation workflow and prompt logic
│   ├── gui/
│   │   ├── common.py        # Shared Qt workers and logging tools
│   │   └── main_window.py   # PySide6 application
│   ├── llm.py               # LLM client implementations and templates
│   └── splitting.py         # Core transcript splitting engine
├── cli.py                   # CLI entry point
├── main.py                  # GUI launcher
└── docs/
    └── ARCHITECTURE.md
````

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CagriCatik/Docalypt.git
   cd Docalypt
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

   Set the desired LLM provider:

   * `DOCALYPT_LLM_PROVIDER=ollama|openai|anthropic`
   * Add API keys and endpoints when using hosted providers.

5. Install and run Ollama (if using local models):

   ```bash
   ollama pull llama3
   ```

## Example workflow: YouTube transcript to chapters and documentation

### 1. Prepare the transcript

Export a YouTube transcript and save it as a single Markdown file:

```text
transcripts/
└── esp32_iot_4_layer_pcb.md
```

Guidelines:

* Accepts plain text or Markdown.
* Timestamps are optional but useful.
* Keep the entire transcript in one file.

### 2. Split chapters using the CLI

```bash
python cli.py transcripts/esp32_iot_4_layer_pcb.md --output-dir ./demo_chapters
```

Output example:

```text
demo_chapters/
├── 000_intro.md
├── 010_schematic_overview.md
├── 020_layer_stackup.md
└── 030_routing_strategies.md
```

### 3. Generate documentation using the GUI

Start the application:

```bash
python main.py
```

In the GUI:

* Load the transcript file.
* Select the chapter output directory.
* Run the split operation.
* Enable LLM generation in the LLM/Ollama tab.
* Refresh and choose a model.
* Optionally adjust generation parameters and the prompt template.
* Select chapters and run documentation generation.

This produces files such as:

```text
demo_chapters/documentation/
├── 000_intro.docs.md
├── 010_schematic_overview.docs.md
├── 020_layer_stackup.docs.md
└── 030_routing_strategies.docs.md
```

Generated documentation is available in [**generated**](./generated/README.md).

## Running Docalypt

### Desktop application

```bash
python main.py
```

Key components:

* Model selection and refresh using the Ollama API.
* Full parameter control: temperature, top-p, max tokens, top-k, penalties.
* Prompt customization with reset support.
* Chapter selection with per-chapter documentation output.

Generated files are saved under:

```bash
<output_dir>/documentation/<chapter>.docs.md
```

### Command-line interface

```bash
python cli.py transcript.md --output-dir ./chapters
```

The CLI uses the same configuration and splitting engine as the GUI.

## Troubleshooting

* Verify that Ollama is running when using local models.
* If models do not appear, check the log panel for API errors.
* Long operations run in worker threads, so the GUI remains responsive. Wait for tasks to complete before closing the window.

## Additional documentation

Detailed architecture notes are available in [**docs**](docs/ARCHITECTURE.md)
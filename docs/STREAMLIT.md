# Streamlit Interface

The Streamlit UI lives in `docalypt/interfaces/streamlit/app.py` and is wired to
`streamlit_app.py` for execution. The app uses the same application services as
the CLI and PySide GUI.

## Pages

The app exposes two tabs:

1. **Split Transcript** – upload a Markdown transcript, choose an output
   directory, and optionally render an HTML index. Splitting uses
   `SplitTranscriptUseCase` with the filesystem repository and reports progress
   through `st.progress`.
2. **Generate Documentation** – select any previously split chapters, adjust
   Ollama settings, and stream documentation generation via
   `GenerateDocumentationUseCase` and the HTTPX-based `OllamaGateway`.

## Session state

- `ui`: stores the loaded `AppConfig` and workspace directory.
- `chapters`: list of chapter paths created during the latest split run.
- `last_split`: metadata about the most recent split (count and HTML path).
- `doc_results`: cached `DocumentOutcome` from the latest documentation run.

## Running locally

```bash
streamlit run streamlit_app.py
```

Set `ST_DEBUG=1` to view detailed logs in the terminal while developing. The app
will gracefully degrade if it cannot reach the local Ollama instance.

"""Streamlit view logic for Docalypt."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import streamlit as st

from docalypt.application.generate_docs import GenerateDocumentationUseCase
from docalypt.application.split_transcript import SplitTranscriptUseCase
from docalypt.domain.services import TranscriptParser
from docalypt.infrastructure.config.toml_loader import AppConfig, load_app_config
from docalypt.infrastructure.llm.ollama import (
    OllamaGateway,
    OllamaSettings,
    list_local_models,
)
from docalypt.infrastructure.storage.filesystem import FileSystemChapterRepository


@dataclass(slots=True)
class UIConfig:
    app_config: AppConfig
    workspace: Path


def init_state() -> UIConfig:
    if "ui" not in st.session_state:
        app_config = load_app_config()
        workspace = Path(st.session_state.get("workspace_dir", app_config.output_dir)).expanduser()
        workspace.mkdir(parents=True, exist_ok=True)
        st.session_state["ui"] = UIConfig(app_config=app_config, workspace=workspace)
        st.session_state.setdefault("chapters", [])
        st.session_state.setdefault("last_split", None)
        st.session_state.setdefault("doc_results", None)
    return st.session_state["ui"]


def run() -> None:
    ui = init_state()
    st.sidebar.header("Ollama")
    try:
        available_models = list_local_models()
    except Exception as exc:  # pragma: no cover - best effort discovery
        available_models = []
        st.sidebar.caption(f"Model discovery failed: {exc}")
    selected_model = (
        st.sidebar.selectbox("Model", available_models) if available_models else st.sidebar.text_input("Model", value="llama3")
    )
    temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.2, 0.1)
    max_tokens = st.sidebar.slider("Max tokens", 200, 4000, 800, 50)

    tabs = st.tabs(["Split Transcript", "Generate Documentation"])

    with tabs[0]:
        st.subheader("1. Upload transcript and split")
        uploaded = st.file_uploader("Markdown transcript", type=["md", "markdown"])
        output_dir = Path(
            st.text_input("Output directory", value=str(ui.workspace))
        ).expanduser()
        marker_regex = st.text_input(
            "Timestamp marker regex",
            value=ui.app_config.marker_regex,
        )
        export_html = st.checkbox("Render HTML index", value=True)

        if uploaded and st.button("Split transcript", type="primary"):
            text = uploaded.getvalue().decode("utf-8")
            pattern = re.compile(marker_regex)
            parser = TranscriptParser(marker_pattern=pattern)
            repository = FileSystemChapterRepository(
                output_dir=output_dir,
                html_template_path=ui.app_config.html_template,
            )
            progress = st.progress(0, text="Splitting transcript")

            def on_progress(current: int, total: int) -> None:
                if total:
                    progress.progress(current / total)

            use_case = SplitTranscriptUseCase(
                parser=parser,
                repository=repository,
                progress_reporter=on_progress,
            )
            output_dir.mkdir(parents=True, exist_ok=True)
            tmp_path = output_dir / "uploaded_transcript.md"
            tmp_path.write_text(text, encoding="utf-8")
            _, written_paths, html_path = use_case.execute(
                input_path=tmp_path,
                export_html=export_html,
                transcript_text=text,
            )
            progress.progress(1.0)
            st.session_state["chapters"] = [str(path) for path in written_paths]
            st.session_state["last_split"] = {
                "count": len(written_paths),
                "html": str(html_path) if html_path else None,
            }
            st.success(f"Split into {len(written_paths)} chapters")
            if html_path:
                st.info(f"HTML index saved to {html_path}")
            for path in written_paths:
                st.write(f"- {path.name}")

    with tabs[1]:
        st.subheader("2. Generate documentation")
        chapters = st.session_state.get("chapters", [])
        if not chapters:
            st.info("Split a transcript first to load chapters.")
        else:
            selected = st.multiselect(
                "Chapters",
                options=chapters,
                default=chapters,
            )
            prompt_template = st.text_area("Custom prompt template", height=200)
            run_button = st.button("Generate documentation", type="primary")
            if run_button:
                settings = OllamaSettings(
                    model=selected_model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                gateway = OllamaGateway(settings=settings)
                use_case = GenerateDocumentationUseCase(gateway=gateway)
                outcome = use_case.execute(
                    chapters=[Path(path) for path in selected],
                    destination_dirname="documentation",
                    prompt_template=prompt_template or None,
                )
                st.session_state["doc_results"] = outcome
                if outcome.written:
                    st.success(f"Generated {len(outcome.written)} documents")
                    for chapter, doc in outcome.written:
                        st.write(f"✅ {chapter.name} -> {doc.name}")
                if outcome.failures:
                    for chapter, message in outcome.failures:
                        st.error(f"❌ {chapter.name}: {message}")


__all__ = ["run"]

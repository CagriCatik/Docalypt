"""Command-line entrypoint wired to the application services."""

from __future__ import annotations

from pathlib import Path

import click

from docalypt.application.generate_docs import GenerateDocumentationUseCase
from docalypt.documentation import DOCUMENTATION_SUBDIR, collect_chapter_files
from docalypt.infrastructure.llm.ollama import OllamaGateway, OllamaSettings
from docalypt.splitting import TranscriptSplitter
def build_splitter(input_path: Path, output_dir: Path | None, marker: str | None, on_progress=None) -> TranscriptSplitter:
    return TranscriptSplitter(
        input_path=input_path,
        output_dir=output_dir,
        marker_regex=marker,
        on_progress=on_progress,
    )


@click.group()
def app() -> None:
    """Docalypt command line tools."""


@app.command("split")
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), help="Output directory")
@click.option("--marker", "-m", help="Custom regex for split markers")
@click.option("--html", "export_html", is_flag=True, help="Also export consolidated HTML")
def split_command(input: Path, output_dir: Path | None, marker: str | None, export_html: bool) -> None:
    """Split a Markdown transcript into chapter files."""

    with click.progressbar(length=1, label="Splitting transcript") as progress:
        state = {"current": 0}

        def on_progress(current: int, total: int) -> None:
            progress.length = max(total, 1)
            delta = max(current, 0) - state["current"]
            if delta:
                progress.update(delta)
                state["current"] = current

        splitter = build_splitter(input, output_dir, marker, on_progress=on_progress)
        count = splitter.split(export_html=export_html)
    click.echo(f"Generated {count} chapter(s) in {splitter.output_dir}")
    if export_html:
        click.echo("HTML index created")


@app.command("docs")
@click.argument("chapters_dir", type=click.Path(exists=True, path_type=Path))
@click.option("--model", default="llama3", show_default=True)
@click.option("--temperature", default=0.2, show_default=True, type=float)
@click.option("--max-tokens", default=800, show_default=True, type=int)
@click.option("--prompt-template", type=click.Path(exists=True, path_type=Path))
def docs_command(
    chapters_dir: Path,
    model: str,
    temperature: float,
    max_tokens: int,
    prompt_template: Path | None,
) -> None:
    """Generate documentation for previously split chapters."""

    settings = OllamaSettings(model=model, temperature=temperature, max_tokens=max_tokens)
    gateway = OllamaGateway(settings=settings)
    use_case = GenerateDocumentationUseCase(gateway=gateway)

    template_text = None
    if prompt_template:
        template_text = prompt_template.read_text(encoding="utf-8")

    chapters = collect_chapter_files(chapters_dir)
    outcome = use_case.execute(
        chapters=chapters,
        destination_dirname=DOCUMENTATION_SUBDIR,
        prompt_template=template_text,
    )

    for chapter, destination in outcome.written:
        click.echo(f"✅ {chapter.name} -> {destination.name}")
    for chapter, message in outcome.failures:
        click.echo(f"❌ {chapter.name}: {message}")

    if outcome.success:
        click.echo("All documents generated successfully!")
    else:
        raise click.ClickException("Some documents failed to generate")


__all__ = ["app", "split_command", "docs_command"]

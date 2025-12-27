"""Command-line interface for Docalypt."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

from docalypt import TranscriptSplitter
from docalypt.documentation import (
    DocumentGenerationRequest,
    collect_chapter_files,
    generate_documentation,
)
from docalypt.env import load_env
from docalypt.llm import PROMPT_TEMPLATE, resolve_system_prompt, settings_from_env

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("docalypt.cli")


@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), help="Output directory")
@click.option("--marker", "-m", help="Custom regex for split markers")
@click.option("--html", "export_html", is_flag=True, help="Also export consolidated HTML")
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
@click.option("--generate-docs", is_flag=True, help="Generate documentation for chapters after splitting.")
@click.option("--docs-only", is_flag=True, help="Skip splitting and only generate documentation for an existing chapters directory.")
@click.option("--system-prompt-file", type=click.Path(path_type=Path), help="Path to a custom system prompt file.")
@click.option("--system-prompt", type=str, help="Inline custom system prompt text.")
@click.option(
    "--system-prompt-allow-empty",
    is_flag=True,
    help="Treat an empty inline system prompt as an intentional override of file/default prompts.",
)
def cli(
    input: Path,
    output_dir: Path | None,
    marker: str | None,
    export_html: bool,
    verbose: bool,
    generate_docs: bool,
    docs_only: bool,
    system_prompt_file: Path | None,
    system_prompt: str | None,
    system_prompt_allow_empty: bool,
) -> None:
    """Split a Markdown transcript into chapter files and optionally generate documentation."""

    load_env()
    if verbose:
        logger.setLevel(logging.DEBUG)

    chapters_dir: Path | None = None
    if docs_only:
        generate_docs = True
        if not input.is_dir():
            logger.error("--docs-only expects INPUT to be a directory of chapter files.")
            sys.exit(1)
        chapters_dir = input

    if not docs_only:
        logger.info("Input: %s", input)
        splitter = TranscriptSplitter(
            input_path=input,
            output_dir=output_dir,
            marker_regex=marker,
        )

        splitter.post_split_hooks = [
            lambda path: logger.info("Created %s", path.name)
        ]

        try:
            count = splitter.split(export_html=export_html)
            chapters_dir = splitter.output_dir
            logger.info("Done! %d chapters generated.", count)
            if export_html:
                logger.info("HTML index created.")
        except Exception as exc:
            logger.error("Error: %s", exc)
            sys.exit(1)

    if not generate_docs:
        return

    if system_prompt_file and not system_prompt_file.exists():
        logger.error("System prompt file does not exist: %s", system_prompt_file)
        sys.exit(1)

    if not chapters_dir:
        logger.error("No chapter directory available for documentation.")
        sys.exit(1)

    chapters = collect_chapter_files(chapters_dir)
    if not chapters:
        logger.error("No chapters found in %s", chapters_dir)
        sys.exit(1)

    settings = settings_from_env()
    settings.system_prompt_text = system_prompt
    settings.system_prompt_file = str(system_prompt_file) if system_prompt_file else None
    settings.system_prompt_allow_empty = system_prompt_allow_empty

    source_description = "default wrapper"
    if system_prompt is not None and (system_prompt.strip() or system_prompt_allow_empty):
        source_description = "inline override"
    elif system_prompt_file:
        source_description = f"file: {system_prompt_file}"

    final_system_prompt = resolve_system_prompt(settings)
    logger.info(
        "Using system prompt source (%s), length: %d characters",
        source_description,
        len(final_system_prompt),
    )

    request = DocumentGenerationRequest(
        chapters=chapters,
        settings=settings,
        prompt_template=PROMPT_TEMPLATE,
    )
    logger.info(
        "Generating documentation with %s (%s) for %d chapters…",
        settings.model or "<model unset>",
        settings.provider,
        len(chapters),
    )
    try:
        result = generate_documentation(request)
    except Exception as exc:  # pragma: no cover - runtime guard
        logger.error("Documentation failed: %s", exc)
        sys.exit(1)

    for chapter, destination in result.written:
        logger.info("Documented %s → %s", chapter.name, destination.name)
    for chapter, error in result.failures:
        logger.error("Failed to document %s: %s", chapter.name, error)
    if result.failures:
        sys.exit(1)


if __name__ == "__main__":
    cli()

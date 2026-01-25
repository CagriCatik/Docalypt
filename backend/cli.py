"""Command-line interface for Docalypt."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

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


def _resolve_markdown_inputs(path: Path) -> list[Path]:
    if path.is_file():
        if path.suffix.lower() != ".md":
            raise FileNotFoundError("Input must be a Markdown file")
        return [path]
    if path.is_dir():
        chapters = collect_chapter_files(path)
        if chapters:
            return chapters
        raise FileNotFoundError(f"No Markdown files found in {path}")
    raise FileNotFoundError(f"Input path does not exist: {path}")


@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
@click.option("--system-prompt", type=str, help="Custom system prompt text.")
@click.option(
    "--system-prompt-allow-empty",
    is_flag=True,
    help="Treat an empty inline system prompt as an intentional override of file/default prompts.",
)
def cli(
    input: Path,
    verbose: bool,
    system_prompt: str | None,
    system_prompt_allow_empty: bool,
) -> None:
    """Generate documentation directly from Markdown files."""

    load_env()
    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        chapters = _resolve_markdown_inputs(input)
    except FileNotFoundError as exc:
        logger.error(str(exc))
        sys.exit(1)

    settings = settings_from_env()
    settings.system_prompt_text = system_prompt
    settings.system_prompt_file = None
    settings.system_prompt_allow_empty = system_prompt_allow_empty

    source_description = "default wrapper"
    if system_prompt is not None and (system_prompt.strip() or system_prompt_allow_empty):
        source_description = "inline override"

    final_system_prompt = resolve_system_prompt(settings)
    logger.info(
        "Using system prompt source (%s), length: %d characters",
        source_description,
        len(final_system_prompt),
    )

    source_root = input if input.is_dir() else input.parent
    request = DocumentGenerationRequest(
        chapters=chapters,
        settings=settings,
        prompt_template=PROMPT_TEMPLATE,
        destination_root=Path.cwd() / "generated",
        source_root=source_root,
    )
    logger.info(
        "Generating documentation with %s (%s) for %d Markdown file(s)...",
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
        logger.info("Documented %s -> %s", chapter.name, destination.name)
    for chapter, error in result.failures:
        logger.error("Failed to document %s: %s", chapter.name, error)
    if result.failures:
        sys.exit(1)


if __name__ == "__main__":
    cli()

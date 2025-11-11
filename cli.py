"""Command-line interface for Docalypt."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import click

from docalypt import TranscriptSplitter
from docalypt.env import load_env

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
def cli(input: Path, output_dir: Path | None, marker: str | None, export_html: bool, verbose: bool) -> None:
    """Split a Markdown transcript into chapter files."""

    load_env()
    if verbose:
        logger.setLevel(logging.DEBUG)

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
        logger.info("Done! %d chapters generated.", count)
        if export_html:
            logger.info("HTML index created.")
    except Exception as exc:
        logger.error("Error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    cli()

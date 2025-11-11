
# File: cli.py
import sys
import logging
import click
from pathlib import Path
from splitter import TranscriptSplitter

# Configure basic CLI logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('input', type=click.Path(exists=True, path_type=Path))
@click.option('--output-dir', '-o', type=click.Path(path_type=Path), help='Output directory')
@click.option('--marker', '-m', help='Custom regex for split markers')
@click.option('--html', 'export_html', is_flag=True, help='Also export consolidated HTML')
@click.option('--verbose', '-v', is_flag=True, help='Verbose logging')
def cli(input: Path, output_dir: Path, marker: str, export_html: bool, verbose: bool):
    """
    Split a Markdown transcript into chapter files.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    logger.info(f"Input: {input}")
    odir = output_dir or None
    splitter = TranscriptSplitter(
        input_path=input,
        output_dir=odir,
        marker_regex=marker
    )

    # Example plugin hook: log each file creation
    splitter.post_split_hooks.append(lambda p: logger.info(f"Created {p.name}"))

    try:
        count = splitter.split(export_html=export_html)
        logger.info(f"Done! {count} chapters generated.")
        if export_html:
            logger.info("HTML index created.")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    cli()

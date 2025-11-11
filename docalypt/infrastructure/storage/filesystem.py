"""Filesystem-backed repository for chapter documents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from jinja2 import Environment, Template

from docalypt.domain.models import ChapterDocument


def _slugify(value: str) -> str:
    return "".join(
        char if char.isalnum() or char in {"_", "-"} else "_" for char in value.lower().replace(" ", "_")
    )


@dataclass(slots=True)
class FileSystemChapterRepository:
    """Persist chapter documents to the local filesystem."""

    output_dir: Path
    html_template_path: Path | None = None

    def save_documents(
        self,
        documents: Sequence[ChapterDocument],
        export_html: bool,
    ) -> tuple[list[Path], Path | None]:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        written: list[Path] = []
        for document in documents:
            filename = f"{document.chapter.index:02d}_{_slugify(document.chapter.title)}.md"
            destination = self.output_dir / filename
            destination.write_text(document.content, encoding="utf-8")
            written.append(destination)

        html_path = self.render_html_index(documents) if export_html else None

        return written, html_path

    def render_html_index(self, documents: Sequence[ChapterDocument]) -> Path:
        return self._render_html_index(documents)

    # Internal helpers -------------------------------------------------
    def _render_html_index(self, documents: Sequence[ChapterDocument]) -> Path:
        template = self._load_template()
        html = template.render(documents=documents)
        destination = self.output_dir / "index.html"
        destination.write_text(html, encoding="utf-8")
        return destination

    def _load_template(self) -> Template:
        if self.html_template_path and self.html_template_path.exists():
            template_text = self.html_template_path.read_text(encoding="utf-8")
        else:
            template_text = _DEFAULT_HTML_TEMPLATE
        env = Environment(autoescape=True)
        return env.from_string(template_text)


_DEFAULT_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <title>Docalypt Chapters</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 2rem; }
      h1 { margin-bottom: 1rem; }
      section { margin-bottom: 2rem; }
      pre { background: #f5f5f5; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; }
    </style>
  </head>
  <body>
    <h1>Transcript Chapters</h1>
    {% for doc in documents %}
      <section>
        <h2>{{ doc.chapter.title }}</h2>
        <pre>{{ doc.content }}</pre>
      </section>
    {% endfor %}
  </body>
</html>
"""


__all__ = ["FileSystemChapterRepository"]

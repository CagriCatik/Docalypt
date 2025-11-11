# File: ollama_helper.py
"""Helper utilities for interacting with a local Ollama instance.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_ENDPOINT = "http://localhost:11434"


@dataclass
class OllamaSettings:
    """Container for Ollama generation settings."""

    model: str
    temperature: float
    max_tokens: int
    top_p: float
    endpoint: str = DEFAULT_ENDPOINT


class OllamaGenerationError(RuntimeError):
    """Raised when Ollama returns an error or the request fails."""


PROMPT_TEMPLATE = """You are assisting with documenting a Markdown Transcript Splitter and Documenter project.
Create a standalone Markdown documentation section for the chapter described below.

Chapter file name: {chapter_name}

Chapter transcript content (verbatim):
```markdown
{chapter_content}
```

Instructions:
- Provide helpful Markdown headings and descriptive prose for this chapter.
- Focus on explaining the chapter context and key takeaways.
- Do not include source code or TODO lists.
- Return only Markdown content suitable for end-user documentation.

"""

def build_prompt(chapter_name: str, chapter_content: str) -> str:
    """Create the prompt sent to Ollama for documentation generation."""

    return PROMPT_TEMPLATE.format(
        chapter_name=chapter_name,
        chapter_content=chapter_content.strip(),
    )


def _perform_request(settings: OllamaSettings, prompt: str) -> str:
    """Send the generation request to the Ollama HTTP API."""

    payload = {
        "model": settings.model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": settings.temperature,
            "top_p": settings.top_p,
            "num_predict": settings.max_tokens,
        },
    }

    request = Request(
        url=f"{settings.endpoint.rstrip('/')}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            collected: list[str] = []
            for raw_line in response:
                if not raw_line:
                    continue
                line = raw_line.decode("utf-8").strip()
                if not line:
                    continue
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError as exc:  # pragma: no cover - defensive
                    raise OllamaGenerationError(f"Invalid response from Ollama: {line}") from exc
                if "error" in chunk:
                    raise OllamaGenerationError(str(chunk["error"]))
                if chunk.get("response"):
                    collected.append(chunk["response"])
                if chunk.get("done"):
                    break
            return "".join(collected).strip()
    except (HTTPError, URLError) as exc:
        raise OllamaGenerationError(str(exc)) from exc


def generate_markdown(prompt: str, settings: OllamaSettings) -> str:
    """Generate Markdown text from Ollama using the provided prompt."""

    if not settings.model.strip():
        raise OllamaGenerationError("No model name provided.")
    return _perform_request(settings, prompt)


def document_chapter(chapter_path: Path, settings: OllamaSettings) -> Path:
    """Generate documentation for a single chapter file and save it.

    Returns the path to the written documentation file.
    """

    chapter_text = chapter_path.read_text(encoding="utf-8")
    prompt = build_prompt(chapter_path.name, chapter_text)
    markdown = generate_markdown(prompt, settings)
    output_path = chapter_path.with_name(f"{chapter_path.stem}.docs.md")
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def document_chapters(
    chapters: Iterable[Path],
    settings: OllamaSettings,
) -> list[Path]:
    """Generate documentation for multiple chapters and return the written files."""

    written: list[Path] = []
    for chapter in chapters:
        written.append(document_chapter(chapter, settings))
    return written


__all__ = [
    "OllamaSettings",
    "OllamaGenerationError",
    "build_prompt",
    "generate_markdown",
    "document_chapter",
    "document_chapters",
]

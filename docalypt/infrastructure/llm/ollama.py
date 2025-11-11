"""HTTPX-based gateway for talking to Ollama."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import httpx

from docalypt.domain.models import DocumentOutcome

DEFAULT_ENDPOINT = "http://localhost:11434"


@dataclass(slots=True)
class OllamaSettings:
    model: str
    temperature: float = 0.2
    max_tokens: int = 800
    top_p: float = 0.9
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    repeat_penalty: float = 1.0
    top_k: int = 40
    endpoint: str = DEFAULT_ENDPOINT


class OllamaError(RuntimeError):
    """Raised when Ollama returns an error or cannot be reached."""


PROMPT_TEMPLATE = """You are helping maintain the Docalypt Markdown Transcript Splitter and Documentation suite.
Create a standalone Markdown documentation section for the chapter below.

Chapter file name: {chapter_name}

Chapter transcript content:
```markdown
{chapter_content}
```

Guidelines:
- Use helpful headings and paragraphs.
- Summarize the narrative and highlight key ideas.
- Do not include code snippets or TODO lists.
- Respond with valid Markdown only.
"""


@dataclass(slots=True)
class OllamaGateway:
    """Generate documentation for chapters using Ollama."""

    settings: OllamaSettings

    def generate_documents(
        self,
        job_chapters: Sequence[Path],
        destination_dirname: str,
        prompt_template: str | None,
    ) -> DocumentOutcome:
        written: list[tuple[Path, Path]] = []
        failures: list[tuple[Path, str]] = []
        template = prompt_template or PROMPT_TEMPLATE

        with httpx.Client(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
            for chapter in job_chapters:
                chapter = Path(chapter)
                try:
                    prompt = build_prompt(
                        chapter.name,
                        chapter.read_text(encoding="utf-8"),
                        template,
                    )
                    markdown = self._stream_completion(client, prompt)
                    destination_dir = chapter.parent / destination_dirname
                    destination_dir.mkdir(parents=True, exist_ok=True)
                    destination = destination_dir / f"{chapter.stem}.docs.md"
                    destination.write_text(markdown, encoding="utf-8")
                    written.append((chapter, destination))
                except Exception as exc:  # noqa: BLE001 - bubble up domain errors
                    failures.append((chapter, str(exc)))
        return DocumentOutcome(written=written, failures=failures)

    # Internal helpers -------------------------------------------------
    def _stream_completion(self, client: httpx.Client, prompt: str) -> str:
        payload = {
            "model": self.settings.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.settings.temperature,
                "top_p": self.settings.top_p,
                "num_predict": self.settings.max_tokens,
                "presence_penalty": self.settings.presence_penalty,
                "frequency_penalty": self.settings.frequency_penalty,
                "repeat_penalty": self.settings.repeat_penalty,
                "top_k": self.settings.top_k,
            },
        }
        url = f"{self.settings.endpoint.rstrip('/')}/api/generate"
        request = client.build_request("POST", url, json=payload)
        with client.send(request, stream=True) as stream:
            stream.raise_for_status()
            pieces: list[str] = []
            for line in stream.iter_lines():
                if not line:
                    continue
                chunk = stream.json_loads(line)
                if "error" in chunk:
                    raise OllamaError(str(chunk["error"]))
                text = chunk.get("response")
                if text:
                    pieces.append(text)
                if chunk.get("done"):
                    break
        return "".join(pieces).strip()


def build_prompt(chapter_name: str, chapter_content: str, template: str = PROMPT_TEMPLATE) -> str:
    if "{chapter_name}" not in template or "{chapter_content}" not in template:
        raise OllamaError(
            "Prompt template must include {chapter_name} and {chapter_content} placeholders",
        )
    return template.format(
        chapter_name=chapter_name,
        chapter_content=chapter_content.strip(),
    )


def list_local_models(endpoint: str = DEFAULT_ENDPOINT) -> list[str]:
    with httpx.Client(timeout=httpx.Timeout(10.0, connect=5.0)) as client:
        response = client.get(f"{endpoint.rstrip('/')}/api/tags")
        response.raise_for_status()
        payload = response.json()
    models: list[str] = []
    for model in payload.get("models", []):
        name = model.get("model") or model.get("name")
        if isinstance(name, str) and name.strip():
            models.append(name.strip())
    return sorted(dict.fromkeys(models))


__all__ = [
    "DEFAULT_ENDPOINT",
    "OllamaError",
    "OllamaGateway",
    "OllamaSettings",
    "PROMPT_TEMPLATE",
    "build_prompt",
    "list_local_models",
]

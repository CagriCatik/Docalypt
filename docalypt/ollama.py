"""Utilities for interacting with a local Ollama instance."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_ENDPOINT = "http://localhost:11434"


@dataclass(slots=True)
class OllamaSettings:
    model: str
    temperature: float = 0.2
    max_tokens: int = 800
    top_p: float = 0.9
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


def build_prompt(chapter_name: str, chapter_content: str) -> str:
    return PROMPT_TEMPLATE.format(
        chapter_name=chapter_name,
        chapter_content=chapter_content.strip(),
    )


class OllamaClient:
    """Simple HTTP client for streaming responses from Ollama."""

    def __init__(self, settings: OllamaSettings):
        if not settings.model.strip():
            raise OllamaError("Model name must not be empty")
        self.settings = settings

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.settings.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.settings.temperature,
                "top_p": self.settings.top_p,
                "num_predict": self.settings.max_tokens,
            },
        }
        request = Request(
            url=f"{self.settings.endpoint.rstrip('/')}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=120) as response:
                pieces: list[str] = []
                for raw_line in response:
                    if not raw_line:
                        continue
                    line = raw_line.decode("utf-8").strip()
                    if not line:
                        continue
                    chunk = json.loads(line)
                    if "error" in chunk:
                        raise OllamaError(str(chunk["error"]))
                    text = chunk.get("response")
                    if text:
                        pieces.append(text)
                    if chunk.get("done"):
                        break
                return "".join(pieces).strip()
        except (HTTPError, URLError) as exc:
            raise OllamaError(str(exc)) from exc
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise OllamaError("Invalid response from Ollama") from exc


__all__ = [
    "OllamaClient",
    "OllamaError",
    "OllamaSettings",
    "build_prompt",
    "DEFAULT_ENDPOINT",
]

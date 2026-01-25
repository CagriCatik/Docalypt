"""Utilities for interacting with local and hosted LLM providers."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_OLLAMA_ENDPOINT = "http://localhost:11434"
DEFAULT_OPENAI_ENDPOINT = "https://api.openai.com/v1"
DEFAULT_ANTHROPIC_ENDPOINT = "https://api.anthropic.com/v1"
DEFAULT_ANTHROPIC_VERSION = "2023-06-01"


ENV_PROVIDER = "DOCALYPT_LLM_PROVIDER"
ENV_MODEL = "DOCALYPT_LLM_MODEL"
ENV_ENDPOINT = "DOCALYPT_LLM_ENDPOINT"
ENV_OPENAI_KEY = "DOCALYPT_OPENAI_API_KEY"
ENV_OPENAI_ENDPOINT = "DOCALYPT_OPENAI_BASE_URL"
ENV_ANTHROPIC_KEY = "DOCALYPT_ANTHROPIC_API_KEY"
ENV_ANTHROPIC_ENDPOINT = "DOCALYPT_ANTHROPIC_BASE_URL"
ENV_ANTHROPIC_VERSION = "DOCALYPT_ANTHROPIC_VERSION"

LEGACY_OPENAI_KEY = "OPENAI_API_KEY"
LEGACY_OPENAI_ENDPOINT = "OPENAI_BASE_URL"
LEGACY_ANTHROPIC_KEY = "ANTHROPIC_API_KEY"
LEGACY_ANTHROPIC_ENDPOINT = "ANTHROPIC_BASE_URL"


class LLMError(RuntimeError):
    """Raised when a model provider returns an error or cannot be reached."""


@dataclass(slots=True)
class LLMSettings:
    provider: str = "ollama"
    model: str = ""
    temperature: float = 0.2
    max_tokens: int = 5000
    top_p: float = 0.9
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    repeat_penalty: float = 1.0
    top_k: int = 40
    endpoint: str | None = None
    api_key: str | None = None
    anthropic_version: str | None = None
    system_prompt_text: str | None = None
    system_prompt_file: str | None = None
    system_prompt_allow_empty: bool = False

    def normalized_provider(self) -> str:
        provider = (self.provider or "ollama").strip().lower()
        if provider not in {"ollama", "openai", "anthropic"}:
            raise LLMError(f"Unsupported provider: {self.provider}")
        return provider

    def resolved_endpoint(self) -> str:
        provider = self.normalized_provider()
        endpoint = (self.endpoint or "").strip()
        if provider == "ollama":
            return endpoint or DEFAULT_OLLAMA_ENDPOINT
        if provider == "openai":
            return endpoint or os.getenv(ENV_OPENAI_ENDPOINT) or os.getenv(LEGACY_OPENAI_ENDPOINT) or DEFAULT_OPENAI_ENDPOINT
        if provider == "anthropic":
            return (
                endpoint
                or os.getenv(ENV_ANTHROPIC_ENDPOINT)
                or os.getenv(LEGACY_ANTHROPIC_ENDPOINT)
                or DEFAULT_ANTHROPIC_ENDPOINT
            )
        raise LLMError(f"Unsupported provider: {self.provider}")

    def resolved_api_key(self) -> str | None:
        provider = self.normalized_provider()
        if provider == "openai":
            return (self.api_key or os.getenv(ENV_OPENAI_KEY) or os.getenv(LEGACY_OPENAI_KEY) or "").strip() or None
        if provider == "anthropic":
            return (
                self.api_key
                or os.getenv(ENV_ANTHROPIC_KEY)
                or os.getenv(LEGACY_ANTHROPIC_KEY)
                or ""
            ).strip() or None
        return (self.api_key or "").strip() or None

    def resolved_anthropic_version(self) -> str:
        return (
            self.anthropic_version
            or os.getenv(ENV_ANTHROPIC_VERSION)
            or DEFAULT_ANTHROPIC_VERSION
        )


PROMPT_TEMPLATE = """Analyze the transcript segment and produce professional documentation strictly from the provided source.

Output rules (strict):
- Use Markdown.
- Do NOT add a title line.
- Headings must emerge dynamically from the transcript content.
- Use headings (##, ###) only where a new conceptual section begins.
- Each heading may appear only once.
- Do not add advice, best practices, or steps unless explicitly stated in the transcript.
- Do not include meta-commentary about the transcript.

Guidelines:
- Preserve the logical order of the conversation.
- Merge repetitions but do not drop any important detail.
- Write as a domain expert, but only using details present in the transcript.
- Use precise terminology from the transcript and explain relationships/context when stated.
- Keep a neutral, clear documentation style.
- If information is missing, write: Not provided in sources.

--- BEGIN SOURCE CONTENT ---
{chapter_content}
--- END SOURCE CONTENT ---
"""


REQUIRED_SYSTEM_WRAPPER = """You are a documentation generator and subject-matter expert.

Non-negotiable rules:

* Use ONLY the provided SOURCES. Do not use external knowledge.
* Do not invent facts. If something is missing, write: Not provided in sources.
* Do not rely on timestamps or timecodes. Do not structure content around timestamps.
* Headings must emerge from the transcript content; use headings only when a new conceptual section begins.
* Each heading may appear only once.
* Preserve logical order and merge repetitions without losing details.
* Write in a professional documentation tone using domain terminology from the transcript.
* Do not include meta-commentary about the transcript."""


def build_prompt(
    chapter_name: str,
    chapter_content: str,
    template: str = PROMPT_TEMPLATE,
) -> str:
    if "{chapter_content}" not in template:
        raise LLMError(
            "Prompt template must include {chapter_content} placeholder"
        )
    # chapter_name is optional
    return template.format(
        chapter_name=chapter_name,
        chapter_content=chapter_content.strip(),
    )


def resolve_system_prompt(config: LLMSettings) -> str:
    """Resolve the effective system prompt, always prepending the required wrapper."""

    inline_prompt = None
    if config.system_prompt_text is not None:
        if config.system_prompt_text.strip() or config.system_prompt_allow_empty:
            inline_prompt = config.system_prompt_text

    file_prompt = None
    if inline_prompt is None and config.system_prompt_file:
        path = Path(config.system_prompt_file).expanduser()
        if path.exists():
            try:
                file_prompt = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                file_prompt = ""

    user_prompt = inline_prompt if inline_prompt is not None else file_prompt
    if user_prompt is None:
        user_prompt = ""

    suffix = f"\n\n{user_prompt}" if (user_prompt.strip() or config.system_prompt_allow_empty) else ""
    return f"{REQUIRED_SYSTEM_WRAPPER}{suffix}"


ChatMessage = Dict[str, str]


def _split_system_from_messages(messages: Sequence[ChatMessage]) -> tuple[str | None, list[ChatMessage]]:
    """Extract a single system prompt for providers that expect a top-level field."""

    system_prompt: str | None = None
    converted: list[ChatMessage] = []
    for message in messages:
        role = message.get("role") if isinstance(message, dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        if role == "system" and system_prompt is None:
            if isinstance(content, str):
                system_prompt = content
            continue
        converted.append({"role": role or "user", "content": content or ""})
    return system_prompt, converted


class _BaseLLMClient:
    def __init__(self, settings: LLMSettings) -> None:
        self.settings = settings

    def generate(self, messages: Sequence[ChatMessage]) -> str:  # pragma: no cover - interface only
        raise NotImplementedError


class _OllamaClient(_BaseLLMClient):
    def generate(self, messages: Sequence[ChatMessage]) -> str:
        model = self.settings.model.strip()
        if not model:
            raise LLMError("Model name must not be empty")
        payload = {
            "model": model,
            "messages": list(messages),
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
        request = Request(
            url=f"{self.settings.resolved_endpoint().rstrip('/')}/api/chat",
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
                        raise LLMError(str(chunk["error"]))
                    message = chunk.get("message")
                    content = None
                    if isinstance(message, dict):
                        content = message.get("content")
                    if isinstance(content, str):
                        pieces.append(content)
                    if chunk.get("done"):
                        break
                return "".join(pieces).strip()
        except (HTTPError, URLError) as exc:
            raise LLMError(str(exc)) from exc
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise LLMError("Invalid response from Ollama") from exc


class _OpenAIClient(_BaseLLMClient):
    def generate(self, messages: Sequence[ChatMessage]) -> str:
        model = self.settings.model.strip()
        if not model:
            raise LLMError("Model name must not be empty")
        api_key = self.settings.resolved_api_key()
        if not api_key:
            raise LLMError("OpenAI API key is required for this provider")
        endpoint = self.settings.resolved_endpoint().rstrip("/")
        payload: Dict[str, object] = {
            "model": model,
            "temperature": self.settings.temperature,
            "max_tokens": self.settings.max_tokens,
            "top_p": self.settings.top_p,
            "presence_penalty": self.settings.presence_penalty,
            "frequency_penalty": self.settings.frequency_penalty,
            "messages": list(messages),
        }
        request = Request(
            url=f"{endpoint}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=120) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError) as exc:
            raise LLMError(str(exc)) from exc
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise LLMError("Invalid response from OpenAI") from exc

        if "error" in payload:
            error = payload["error"]
            if isinstance(error, dict) and "message" in error:
                raise LLMError(str(error["message"]))
            raise LLMError(str(error))

        choices = payload.get("choices")
        if not isinstance(choices, list):
            raise LLMError("OpenAI response missing choices")
        pieces: List[str] = []
        for choice in choices:
            message = choice.get("message") if isinstance(choice, dict) else None
            if isinstance(message, dict):
                content = message.get("content")
                if isinstance(content, str):
                    pieces.append(content)
        if not pieces:
            raise LLMError("OpenAI response did not include any content")
        return "\n".join(piece.strip() for piece in pieces if piece).strip()


class _AnthropicClient(_BaseLLMClient):
    def generate(self, messages: Sequence[ChatMessage]) -> str:
        model = self.settings.model.strip()
        if not model:
            raise LLMError("Model name must not be empty")
        api_key = self.settings.resolved_api_key()
        if not api_key:
            raise LLMError("Anthropic API key is required for this provider")
        endpoint = self.settings.resolved_endpoint().rstrip("/")
        system_prompt, anthropic_messages = _split_system_from_messages(messages)
        payload: Dict[str, object] = {
            "model": model,
            "max_tokens": self.settings.max_tokens,
            "temperature": self.settings.temperature,
            "top_p": self.settings.top_p,
            "top_k": self.settings.top_k,
            "presence_penalty": self.settings.presence_penalty,
            "frequency_penalty": self.settings.frequency_penalty,
            "messages": anthropic_messages,
        }
        if system_prompt is not None:
            payload["system"] = system_prompt
        request = Request(
            url=f"{endpoint}/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": self.settings.resolved_anthropic_version(),
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=120) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError) as exc:
            raise LLMError(str(exc)) from exc
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            raise LLMError("Invalid response from Anthropic") from exc

        if "error" in payload:
            error = payload["error"]
            if isinstance(error, dict) and "message" in error:
                raise LLMError(str(error["message"]))
            raise LLMError(str(error))

        content = payload.get("content")
        if not isinstance(content, list):
            raise LLMError("Anthropic response missing content")
        pieces: List[str] = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text" and isinstance(block.get("text"), str):
                pieces.append(block["text"])
        if not pieces:
            raise LLMError("Anthropic response did not include any text blocks")
        return "\n".join(piece.strip() for piece in pieces if piece).strip()


def create_client(settings: LLMSettings) -> _BaseLLMClient:
    provider = settings.normalized_provider()
    if provider == "ollama":
        return _OllamaClient(settings)
    if provider == "openai":
        return _OpenAIClient(settings)
    if provider == "anthropic":
        return _AnthropicClient(settings)
    raise LLMError(f"Unsupported provider: {settings.provider}")


def list_models(settings: LLMSettings) -> list[str]:
    provider = settings.normalized_provider()
    if provider == "ollama":
        return _list_local_models(settings.resolved_endpoint())
    if provider == "openai":
        return _list_openai_models(settings)
    # Anthropic and other providers do not expose a public model listing endpoint.
    return []


def _list_local_models(endpoint: str) -> list[str]:
    request = Request(
        url=f"{endpoint.rstrip('/')}/api/tags",
        headers={"Accept": "application/json"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise LLMError(str(exc)) from exc
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise LLMError("Invalid response from Ollama") from exc

    models: List[str] = []
    for model in payload.get("models", []):
        name = model.get("model") if isinstance(model, dict) else None
        if not name and isinstance(model, dict):
            name = model.get("name")
        if isinstance(name, str) and name.strip():
            models.append(name.strip())

    unique_sorted = sorted(dict.fromkeys(models))
    return unique_sorted


def _list_openai_models(settings: LLMSettings) -> list[str]:
    api_key = settings.resolved_api_key()
    if not api_key:
        raise LLMError("OpenAI API key is required to fetch model list")
    endpoint = settings.resolved_endpoint().rstrip("/")
    request = Request(
        url=f"{endpoint}/models",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise LLMError(str(exc)) from exc
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise LLMError("Invalid response from OpenAI") from exc

    data = payload.get("data")
    if not isinstance(data, list):
        raise LLMError("OpenAI response missing model list")

    models: List[str] = []
    for model in data:
        if isinstance(model, dict):
            identifier = model.get("id")
            if isinstance(identifier, str) and identifier.strip():
                models.append(identifier.strip())
    return sorted(dict.fromkeys(models))


def settings_from_env() -> LLMSettings:
    provider = os.getenv(ENV_PROVIDER, "ollama")
    model = os.getenv(ENV_MODEL, "llama3")
    endpoint = os.getenv(ENV_ENDPOINT)
    provider_lower = (provider or "ollama").strip().lower()

    if provider_lower == "openai":
        endpoint = (
            endpoint
            or os.getenv(ENV_OPENAI_ENDPOINT)
            or os.getenv(LEGACY_OPENAI_ENDPOINT)
        )
        api_key = os.getenv(ENV_OPENAI_KEY) or os.getenv(LEGACY_OPENAI_KEY)
    elif provider_lower == "anthropic":
        endpoint = (
            endpoint
            or os.getenv(ENV_ANTHROPIC_ENDPOINT)
            or os.getenv(LEGACY_ANTHROPIC_ENDPOINT)
        )
        api_key = os.getenv(ENV_ANTHROPIC_KEY) or os.getenv(LEGACY_ANTHROPIC_KEY)
    else:
        api_key = None

    return LLMSettings(
        provider=provider,
        model=model,
        endpoint=endpoint,
        api_key=api_key,
        anthropic_version=os.getenv(ENV_ANTHROPIC_VERSION, DEFAULT_ANTHROPIC_VERSION),
    )


# Backwards compatible aliases -------------------------------------------------
OllamaSettings = LLMSettings
OllamaError = LLMError


__all__ = [
    "DEFAULT_ANTHROPIC_ENDPOINT",
    "DEFAULT_ANTHROPIC_VERSION",
    "DEFAULT_OLLAMA_ENDPOINT",
    "DEFAULT_OPENAI_ENDPOINT",
    "ChatMessage",
    "LLMError",
    "LLMSettings",
    "OllamaError",
    "OllamaSettings",
    "PROMPT_TEMPLATE",
    "REQUIRED_SYSTEM_WRAPPER",
    "build_prompt",
    "create_client",
    "list_models",
    "resolve_system_prompt",
    "settings_from_env",
]

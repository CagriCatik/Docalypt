from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docalypt.llm import LLMSettings, REQUIRED_SYSTEM_WRAPPER, resolve_system_prompt


def test_default_wrapper_only() -> None:
    settings = LLMSettings()
    prompt = resolve_system_prompt(settings)
    assert prompt == REQUIRED_SYSTEM_WRAPPER


def test_inline_override_appends_after_wrapper() -> None:
    settings = LLMSettings(system_prompt_text="Custom system")
    prompt = resolve_system_prompt(settings)
    assert prompt.startswith(REQUIRED_SYSTEM_WRAPPER)
    assert prompt.endswith("Custom system")


def test_file_override(tmp_path: Path) -> None:
    system_path = tmp_path / "system.txt"
    system_path.write_text("File system prompt", encoding="utf-8")
    settings = LLMSettings(system_prompt_file=str(system_path))
    prompt = resolve_system_prompt(settings)
    assert prompt.endswith("File system prompt")


def test_inline_precedence_over_file(tmp_path: Path) -> None:
    system_path = tmp_path / "system.txt"
    system_path.write_text("File content", encoding="utf-8")
    settings = LLMSettings(system_prompt_text="Inline content", system_prompt_file=str(system_path))
    prompt = resolve_system_prompt(settings)
    assert prompt.endswith("Inline content")
    assert "File content" not in prompt


def test_empty_inline_falls_back_to_file(tmp_path: Path) -> None:
    system_path = tmp_path / "system.txt"
    system_path.write_text("File content", encoding="utf-8")
    settings = LLMSettings(system_prompt_text="   ", system_prompt_file=str(system_path))
    prompt = resolve_system_prompt(settings)
    assert prompt.endswith("File content")


def test_allow_empty_preserves_wrapper(tmp_path: Path) -> None:
    settings = LLMSettings(system_prompt_text="", system_prompt_allow_empty=True)
    prompt = resolve_system_prompt(settings)
    assert prompt == f"{REQUIRED_SYSTEM_WRAPPER}\n\n"
    assert "Do not rely on timestamps or timecodes." in prompt

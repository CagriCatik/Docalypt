from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture()
def api_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    transcripts_dir = tmp_path / "transcripts"
    generated_dir = tmp_path / "generated"
    prompts_dir = tmp_path / "prompts"
    transcripts_dir.mkdir()
    generated_dir.mkdir()
    prompts_dir.mkdir()

    monkeypatch.setenv("DOCALYPT_TRANSCRIPTS_DIR", str(transcripts_dir))
    monkeypatch.setenv("DOCALYPT_GENERATED_DIR", str(generated_dir))
    monkeypatch.setenv("DOCALYPT_PROMPTS_DIR", str(prompts_dir))
    monkeypatch.setenv("DOCALYPT_CORS_ORIGINS", "http://example.test")

    if "server" in sys.modules:
        importlib.reload(sys.modules["server"])
    else:
        import server  # noqa: F401

    app = sys.modules["server"].app
    return TestClient(app)

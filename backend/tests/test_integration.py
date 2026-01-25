from __future__ import annotations

import os
from pathlib import Path

import server
from docalypt import documentation


class StubClient:
    def generate(self, messages):
        return "Generated documentation"


def test_get_config(api_client):
    response = api_client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert data["provider"]
    assert "model" in data
    assert "system_prompt" in data
    assert "prompt_template" in data


def test_get_models(api_client, monkeypatch):
    monkeypatch.setattr(server, "list_models", lambda settings: ["model-a", "model-b"])
    response = api_client.get("/api/models")
    assert response.status_code == 200
    data = response.json()
    assert data["models"] == ["model-a", "model-b"]


def test_upload_and_list_files(api_client):
    content = "# Sample\nContent"
    response = api_client.post(
        "/api/upload",
        files={"file": ("sample.md", content, "text/markdown")},
    )
    assert response.status_code == 200
    files_response = api_client.get("/api/files")
    assert files_response.status_code == 200
    files = files_response.json()["files"]
    assert any(item["name"] == "sample.md" for item in files)


def test_split_by_headings(api_client):
    transcript = "# Intro\nHi\n\n# Chapter One\nDetails\n"
    api_client.post(
        "/api/upload",
        files={"file": ("split.md", transcript, "text/markdown")},
    )
    response = api_client.post("/api/split", json={"filename": "split.md"})
    assert response.status_code == 200
    data = response.json()
    assert data["chapters"]
    assert data["chapters"][0]["title"] == "1. Intro"


def test_generate_docs_with_stubbed_llm(api_client, monkeypatch):
    transcript_dir = Path(os.environ["DOCALYPT_TRANSCRIPTS_DIR"])
    path = transcript_dir / "gen.md"
    path.write_text("# Chapter\nContent", encoding="utf-8")

    monkeypatch.setattr(documentation, "create_client", lambda settings: StubClient())

    payload = {
        "req": {"files": ["gen.md"], "standalone": False},
        "config": {"model": "stub-model"},
    }
    response = api_client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["success"] is True


def test_prompts_list_and_fetch(api_client):
    prompts_dir = Path(os.environ["DOCALYPT_PROMPTS_DIR"])
    prompt_path = prompts_dir / "sample_prompt.md"
    prompt_path.write_text("# Sample Prompt\nHello", encoding="utf-8")

    response = api_client.get("/api/prompts")
    assert response.status_code == 200
    prompts = response.json()["prompts"]
    assert any(prompt["name"] == "sample_prompt.md" for prompt in prompts)

    content_response = api_client.get("/api/prompts/sample_prompt.md")
    assert content_response.status_code == 200
    content = content_response.json()["content"]
    assert "Sample Prompt" in content

from __future__ import annotations

import os
from pathlib import Path

from docalypt import documentation


class StubClient:
    def generate(self, messages):
        return "Stubbed output"


def test_api_config_transmission(api_client):
    response = api_client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "provider" in data
    assert "model" in data
    assert "system_prompt" in data
    assert "prompt_template" in data


def test_full_transmission_lifecycle(api_client):
    transcript_content = """# Introduction
This is the intro.

# Technical Segment
Details about the architecture.

# Conclusion
Final thoughts.
"""
    transcript_name = "transmission_test.md"

    response = api_client.post(
        "/api/upload",
        files={"file": (transcript_name, transcript_content, "text/markdown")},
    )
    assert response.status_code == 200
    assert response.json()["filename"] == transcript_name

    response = api_client.post("/api/split", json={"filename": transcript_name})
    assert response.status_code == 200
    chapters = response.json()["chapters"]
    titles = [c["title"] for c in chapters]
    assert "1. Introduction" in titles
    assert "2. Technical Segment" in titles
    assert "3. Conclusion" in titles


def test_generate_requires_valid_input(api_client):
    response = api_client.post("/api/generate", json={
        "req": {"files": []},
        "config": {"model": "test-model"},
    })
    assert response.status_code == 400
    assert "No valid files selected" in response.json()["detail"]


def test_multi_file_generation(api_client, monkeypatch):
    transcript_dir = Path(os.environ["DOCALYPT_TRANSCRIPTS_DIR"])
    transcript_dir.mkdir(parents=True, exist_ok=True)
    (transcript_dir / "chap1.md").write_text("# Chapter 1\nContent 1", encoding="utf-8")
    (transcript_dir / "chap2.md").write_text("# Chapter 2\nContent 2", encoding="utf-8")

    monkeypatch.setattr(documentation, "create_client", lambda settings: StubClient())

    response = api_client.post("/api/generate", json={
        "req": {
            "files": ["chap1.md", "chap2.md"],
            "standalone": False
        },
        "config": {"model": "test-model"},
    })

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["generated"]) == 2


def test_standalone_generation(api_client, monkeypatch):
    transcript_dir = Path(os.environ["DOCALYPT_TRANSCRIPTS_DIR"])
    (transcript_dir / "solo1.md").write_text("# Chapter 1\nContent 1", encoding="utf-8")
    (transcript_dir / "solo2.md").write_text("# Chapter 2\nContent 2", encoding="utf-8")

    monkeypatch.setattr(documentation, "create_client", lambda settings: StubClient())

    response = api_client.post("/api/generate", json={
        "req": {
            "files": ["solo1.md", "solo2.md"],
            "standalone": True
        },
        "config": {"model": "test-model"},
    })

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["generated"]) == 1

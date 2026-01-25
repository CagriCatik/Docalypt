from __future__ import annotations


def test_open_folder_enabled(api_client):
    response = api_client.post("/api/open-folder", json={"type": "transcripts"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"


def test_upload_rejects_path_traversal(api_client):
    response = api_client.post(
        "/api/upload",
        files={"file": ("../evil.md", "# x", "text/markdown")},
    )
    assert response.status_code == 400


def test_prompt_path_traversal_rejected(api_client):
    response = api_client.get("/api/prompts/../secrets.md")
    assert response.status_code in {400, 404}


def test_delete_rejects_path_traversal(api_client):
    response = api_client.request("DELETE", "/api/files", json={"files": ["../evil.md"]})
    assert response.status_code == 200
    payload = response.json()
    assert payload["failed"]
    assert "Invalid path" in payload["failed"][0]

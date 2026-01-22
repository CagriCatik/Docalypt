"""Comprehensive tests for Docalypt Web API.

Tests cover:
- API Health and Session Management
- File Upload and Validation
- Transcript Splitting
- LLM Configuration and Model Listing
- Documentation Generation
- Download and Export
- Error Handling and Edge Cases
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from web.api import app, sessions, UPLOAD_DIR, OUTPUT_DIR


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def clean_sessions():
    """Clean sessions before and after each test."""
    sessions.clear()
    yield
    sessions.clear()


@pytest.fixture
def sample_transcript():
    """Create a sample valid transcript content."""
    return """00:00:00 - Introduction
00:05:30 - Main Content
00:15:00 - Conclusion

Transcript:

(00:00:05) Welcome to this tutorial about Python programming.

(00:00:30) Today we will learn about functions and classes.

(00:05:35) Let's start with the main content of our lesson.

(00:05:50) Functions are reusable blocks of code.

(00:15:05) In conclusion, we covered a lot of ground today.

(00:15:30) Thank you for watching.
"""


@pytest.fixture
def session_with_file(client, clean_sessions, sample_transcript):
    """Create a session with an uploaded file."""
    # Create session
    response = client.post("/api/sessions")
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    
    # Upload file
    files = {"file": ("transcript.md", sample_transcript, "text/markdown")}
    response = client.post(f"/api/upload?session_id={session_id}", files=files)
    assert response.status_code == 200
    
    return session_id


# =============================================================================
# Health Check Tests
# =============================================================================

class TestHealthCheck:
    """Tests for health check endpoint."""
    
    def test_health_check_returns_200(self, client):
        """Health check should return 200 status."""
        response = client.get("/api/health")
        assert response.status_code == 200
    
    def test_health_check_response_structure(self, client):
        """Health check response should have correct structure."""
        response = client.get("/api/health")
        data = response.json()
        
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert data["status"] == "healthy"
    
    def test_health_check_timestamp_format(self, client):
        """Health check timestamp should be ISO format."""
        response = client.get("/api/health")
        data = response.json()
        
        # ISO format check (basic validation)
        timestamp = data["timestamp"]
        assert "T" in timestamp or "-" in timestamp


# =============================================================================
# Session Management Tests
# =============================================================================

class TestSessionManagement:
    """Tests for session creation and management."""
    
    def test_create_session_returns_201(self, client, clean_sessions):
        """Creating a session should succeed."""
        response = client.post("/api/sessions")
        assert response.status_code == 200
    
    def test_create_session_returns_session_id(self, client, clean_sessions):
        """Create session should return a session ID."""
        response = client.post("/api/sessions")
        data = response.json()
        
        assert "session_id" in data
        assert len(data["session_id"]) == 36  # UUID format
    
    def test_create_session_stores_in_memory(self, client, clean_sessions):
        """Session should be stored in memory."""
        response = client.post("/api/sessions")
        session_id = response.json()["session_id"]
        
        assert session_id in sessions
    
    def test_get_session_existing(self, client, clean_sessions):
        """Getting an existing session should succeed."""
        create_response = client.post("/api/sessions")
        session_id = create_response.json()["session_id"]
        
        response = client.get(f"/api/sessions/{session_id}")
        assert response.status_code == 200
    
    def test_get_session_not_found(self, client, clean_sessions):
        """Getting a non-existent session should return 404."""
        response = client.get("/api/sessions/non-existent-id")
        assert response.status_code == 404
    
    def test_delete_session(self, client, clean_sessions):
        """Deleting a session should succeed."""
        create_response = client.post("/api/sessions")
        session_id = create_response.json()["session_id"]
        
        response = client.delete(f"/api/sessions/{session_id}")
        assert response.status_code == 200
        assert session_id not in sessions
    
    def test_delete_session_not_found(self, client, clean_sessions):
        """Deleting a non-existent session should return 404."""
        response = client.delete("/api/sessions/non-existent-id")
        assert response.status_code == 404


# =============================================================================
# File Upload Tests
# =============================================================================

class TestFileUpload:
    """Tests for file upload functionality."""
    
    def test_upload_markdown_file(self, client, clean_sessions):
        """Uploading a markdown file should succeed."""
        # Create session first
        session_response = client.post("/api/sessions")
        session_id = session_response.json()["session_id"]
        
        # Upload file
        files = {"file": ("test.md", "# Test Content", "text/markdown")}
        response = client.post(f"/api/upload?session_id={session_id}", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.md"
    
    def test_upload_non_markdown_file_rejected(self, client, clean_sessions):
        """Uploading non-markdown files should be rejected."""
        session_response = client.post("/api/sessions")
        session_id = session_response.json()["session_id"]
        
        files = {"file": ("test.txt", "plain text", "text/plain")}
        response = client.post(f"/api/upload?session_id={session_id}", files=files)
        
        assert response.status_code == 400
        assert "Markdown" in response.json()["detail"]
    
    def test_upload_without_session(self, client, clean_sessions):
        """Uploading without a valid session should fail."""
        files = {"file": ("test.md", "# Test", "text/markdown")}
        response = client.post("/api/upload?session_id=invalid", files=files)
        
        assert response.status_code == 404
    
    def test_upload_file_stored(self, client, clean_sessions):
        """Uploaded file should be stored in session."""
        session_response = client.post("/api/sessions")
        session_id = session_response.json()["session_id"]
        
        files = {"file": ("test.md", "# Test Content", "text/markdown")}
        client.post(f"/api/upload?session_id={session_id}", files=files)
        
        assert len(sessions[session_id]["files"]) == 1
        assert sessions[session_id]["files"][0]["filename"] == "test.md"
    
    def test_list_uploaded_files(self, client, clean_sessions):
        """List files should return all uploaded files."""
        session_response = client.post("/api/sessions")
        session_id = session_response.json()["session_id"]
        
        files = {"file": ("test.md", "# Test", "text/markdown")}
        client.post(f"/api/upload?session_id={session_id}", files=files)
        
        response = client.get(f"/api/files/{session_id}")
        assert response.status_code == 200
        assert len(response.json()["files"]) == 1


# =============================================================================
# Transcript Splitting Tests
# =============================================================================

class TestTranscriptSplitting:
    """Tests for transcript splitting functionality."""
    
    def test_split_transcript_valid(self, client, session_with_file):
        """Splitting a valid transcript should succeed."""
        response = client.post(
            "/api/split",
            json={"session_id": session_with_file}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["chapter_count"] > 0
        assert len(data["chapters"]) > 0
    
    def test_split_transcript_returns_chapters(self, client, session_with_file):
        """Split should return chapter information."""
        response = client.post(
            "/api/split",
            json={"session_id": session_with_file}
        )
        
        data = response.json()
        chapters = data["chapters"]
        
        for chapter in chapters:
            assert "index" in chapter
            assert "filename" in chapter
            assert "title" in chapter
            assert "preview" in chapter
    
    def test_split_without_file(self, client, clean_sessions):
        """Split without uploaded file should fail."""
        session_response = client.post("/api/sessions")
        session_id = session_response.json()["session_id"]
        
        response = client.post(
            "/api/split",
            json={"session_id": session_id}
        )
        
        assert response.status_code == 400
        assert "No files" in response.json()["detail"]
    
    def test_split_invalid_session(self, client, clean_sessions):
        """Split with invalid session should return 404."""
        response = client.post(
            "/api/split",
            json={"session_id": "invalid"}
        )
        
        assert response.status_code == 404
    
    def test_get_chapters_after_split(self, client, session_with_file):
        """Getting chapters after split should work."""
        client.post("/api/split", json={"session_id": session_with_file})
        
        response = client.get(f"/api/chapters/{session_with_file}")
        assert response.status_code == 200
        assert "chapters" in response.json()
    
    def test_get_specific_chapter(self, client, session_with_file):
        """Getting a specific chapter should return content."""
        client.post("/api/split", json={"session_id": session_with_file})
        
        response = client.get(f"/api/chapters/{session_with_file}/0")
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
    
    def test_get_chapter_invalid_index(self, client, session_with_file):
        """Getting chapter with invalid index should fail."""
        client.post("/api/split", json={"session_id": session_with_file})
        
        response = client.get(f"/api/chapters/{session_with_file}/999")
        assert response.status_code == 404


# =============================================================================
# LLM Configuration Tests
# =============================================================================

class TestLLMConfiguration:
    """Tests for LLM configuration and model listing."""
    
    def test_get_default_settings(self, client):
        """Getting default settings should succeed."""
        response = client.get("/api/settings/default")
        assert response.status_code == 200
        
        data = response.json()
        assert "provider" in data
        assert "model" in data
        assert "temperature" in data
    
    def test_get_default_settings_values(self, client):
        """Default settings should have expected values."""
        response = client.get("/api/settings/default")
        data = response.json()
        
        assert data["provider"] in ["ollama", "openai", "anthropic"]
        assert 0 <= data["temperature"] <= 2
        assert data["max_tokens"] > 0
    
    @patch("web.api.list_models")
    def test_list_models_ollama(self, mock_list_models, client):
        """Listing Ollama models should succeed when available."""
        mock_list_models.return_value = ["llama3", "codellama", "mistral"]
        
        response = client.get("/api/models?provider=ollama")
        assert response.status_code == 200
        
        data = response.json()
        assert data["provider"] == "ollama"
        assert len(data["models"]) == 3
    
    @patch("web.api.list_models")
    def test_list_models_empty(self, mock_list_models, client):
        """Empty model list should return empty array."""
        mock_list_models.return_value = []
        
        response = client.get("/api/models?provider=ollama")
        assert response.status_code == 200
        assert response.json()["models"] == []
    
    def test_check_providers_status(self, client):
        """Provider status check should return list."""
        response = client.get("/api/providers/status")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # Check each provider has required fields
        for provider in data:
            assert "provider" in provider
            assert "available" in provider
            assert "message" in provider


# =============================================================================
# Documentation Generation Tests
# =============================================================================

class TestDocumentationGeneration:
    """Tests for documentation generation."""
    
    def test_docgen_without_chapters(self, client, clean_sessions):
        """Generating docs without chapters should fail."""
        session_response = client.post("/api/sessions")
        session_id = session_response.json()["session_id"]
        
        response = client.post(
            "/api/docgen",
            json={
                "session_id": session_id,
                "settings": {
                    "provider": "ollama",
                    "model": "llama3"
                }
            }
        )
        
        assert response.status_code == 400
        assert "No chapters" in response.json()["detail"]
    
    def test_docgen_invalid_session(self, client, clean_sessions):
        """Generating docs with invalid session should fail."""
        response = client.post(
            "/api/docgen",
            json={
                "session_id": "invalid",
                "settings": {
                    "provider": "ollama",
                    "model": "llama3"
                }
            }
        )
        
        assert response.status_code == 404
    
    @patch("web.api.generate_documentation")
    def test_docgen_success(self, mock_generate, client, session_with_file):
        """Documentation generation should succeed with mocked LLM."""
        # Split first
        client.post("/api/split", json={"session_id": session_with_file})
        
        # Mock successful generation
        mock_result = MagicMock()
        mock_result.written = [(Path("chapter.md"), Path("chapter.docs.md"))]
        mock_result.failures = []
        mock_generate.return_value = mock_result
        
        response = client.post(
            "/api/docgen",
            json={
                "session_id": session_with_file,
                "settings": {
                    "provider": "ollama",
                    "model": "llama3"
                }
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] == 1
        assert data["failed"] == 0
    
    @patch("web.api.generate_documentation")
    def test_docgen_partial_failure(self, mock_generate, client, session_with_file):
        """Documentation generation with partial failures."""
        client.post("/api/split", json={"session_id": session_with_file})
        
        mock_result = MagicMock()
        mock_result.written = [(Path("good.md"), Path("good.docs.md"))]
        mock_result.failures = [(Path("bad.md"), "LLM error")]
        mock_generate.return_value = mock_result
        
        response = client.post(
            "/api/docgen",
            json={
                "session_id": session_with_file,
                "settings": {
                    "provider": "ollama",
                    "model": "llama3"
                }
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["successful"] == 1
        assert data["failed"] == 1
    
    def test_docgen_with_custom_settings(self, client, session_with_file):
        """Documentation generation should accept custom settings."""
        client.post("/api/split", json={"session_id": session_with_file})
        
        # This will likely fail without actual LLM, but validates settings parsing
        with patch("web.api.generate_documentation") as mock_gen:
            mock_result = MagicMock()
            mock_result.written = []
            mock_result.failures = []
            mock_gen.return_value = mock_result
            
            response = client.post(
                "/api/docgen",
                json={
                    "session_id": session_with_file,
                    "chapter_indices": [0],
                    "settings": {
                        "provider": "openai",
                        "model": "gpt-4",
                        "temperature": 0.5,
                        "max_tokens": 2000,
                        "top_p": 0.95,
                        "top_k": 50
                    }
                }
            )
            
            assert response.status_code == 200


# =============================================================================
# Download Tests
# =============================================================================

class TestDownload:
    """Tests for download functionality."""
    
    def test_download_invalid_session(self, client, clean_sessions):
        """Download with invalid session should fail."""
        response = client.get("/api/download/invalid-session")
        assert response.status_code == 404
    
    def test_get_documentation_empty(self, client, clean_sessions):
        """Getting documentation from empty session."""
        session_response = client.post("/api/sessions")
        session_id = session_response.json()["session_id"]
        
        response = client.get(f"/api/documentation/{session_id}")
        assert response.status_code == 200
        assert response.json()["documentation"] == []


# =============================================================================
# Integration Tests
# =============================================================================

class TestFullWorkflow:
    """Integration tests for the complete workflow."""
    
    def test_full_workflow_split(self, client, sample_transcript, clean_sessions):
        """Test complete upload and split workflow."""
        # 1. Create session
        session_response = client.post("/api/sessions")
        assert session_response.status_code == 200
        session_id = session_response.json()["session_id"]
        
        # 2. Upload file
        files = {"file": ("transcript.md", sample_transcript, "text/markdown")}
        upload_response = client.post(f"/api/upload?session_id={session_id}", files=files)
        assert upload_response.status_code == 200
        
        # 3. Split transcript
        split_response = client.post("/api/split", json={"session_id": session_id})
        assert split_response.status_code == 200
        assert split_response.json()["chapter_count"] > 0
        
        # 4. Get chapters
        chapters_response = client.get(f"/api/chapters/{session_id}")
        assert chapters_response.status_code == 200
        assert len(chapters_response.json()["chapters"]) > 0
    
    @patch("web.api.generate_documentation")
    def test_full_workflow_with_docgen(self, mock_generate, client, sample_transcript, clean_sessions):
        """Test complete workflow including documentation generation."""
        # Setup
        session_response = client.post("/api/sessions")
        session_id = session_response.json()["session_id"]
        
        files = {"file": ("transcript.md", sample_transcript, "text/markdown")}
        client.post(f"/api/upload?session_id={session_id}", files=files)
        client.post("/api/split", json={"session_id": session_id})
        
        # Mock LLM response
        mock_result = MagicMock()
        mock_result.written = [
            (Path("01_intro.md"), Path("01_intro.docs.md")),
            (Path("02_main.md"), Path("02_main.docs.md")),
        ]
        mock_result.failures = []
        mock_generate.return_value = mock_result
        
        # Generate documentation
        docgen_response = client.post(
            "/api/docgen",
            json={
                "session_id": session_id,
                "settings": {"provider": "ollama", "model": "llama3"}
            }
        )
        
        assert docgen_response.status_code == 200
        data = docgen_response.json()
        assert data["successful"] == 2
        assert data["failed"] == 0


# =============================================================================
# Error Handling Tests
# =============================================================================

class TestErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_invalid_json_body(self, client, clean_sessions):
        """Sending invalid JSON should return 422."""
        response = client.post(
            "/api/split",
            content="not valid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_field(self, client, clean_sessions):
        """Missing required fields should return 422."""
        response = client.post(
            "/api/split",
            json={}  # Missing session_id
        )
        assert response.status_code == 422
    
    def test_empty_file_upload(self, client, clean_sessions):
        """Empty file should still be accepted (valid markdown)."""
        session_response = client.post("/api/sessions")
        session_id = session_response.json()["session_id"]
        
        files = {"file": ("empty.md", "", "text/markdown")}
        response = client.post(f"/api/upload?session_id={session_id}", files=files)
        
        # Empty file is technically valid markdown
        assert response.status_code == 200
    
    def test_session_isolation(self, client, clean_sessions, sample_transcript):
        """Sessions should be isolated from each other."""
        # Create two sessions
        session1 = client.post("/api/sessions").json()["session_id"]
        session2 = client.post("/api/sessions").json()["session_id"]
        
        # Upload to session 1
        files = {"file": ("test.md", sample_transcript, "text/markdown")}
        client.post(f"/api/upload?session_id={session1}", files=files)
        
        # Session 2 should have no files
        files_response = client.get(f"/api/files/{session2}")
        assert files_response.json()["files"] == []
        
        # Session 1 should have 1 file
        files_response = client.get(f"/api/files/{session1}")
        assert len(files_response.json()["files"]) == 1


# =============================================================================
# Performance Tests
# =============================================================================

class TestPerformance:
    """Basic performance tests."""
    
    def test_multiple_sessions(self, client, clean_sessions):
        """Creating multiple sessions should work."""
        session_ids = []
        for _ in range(10):
            response = client.post("/api/sessions")
            assert response.status_code == 200
            session_ids.append(response.json()["session_id"])
        
        # All sessions should be unique
        assert len(set(session_ids)) == 10
        
        # All sessions should be accessible
        for sid in session_ids:
            response = client.get(f"/api/sessions/{sid}")
            assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

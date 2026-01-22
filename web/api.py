"""FastAPI backend for Docalypt web application."""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import tempfile
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Optional

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Add parent path to import docalypt modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from docalypt.env import load_env
from docalypt.splitting import TranscriptSplitter, Chapter, SplitResult
from docalypt.documentation import (
    DocumentGenerationRequest,
    DocumentGenerationResult,
    collect_chapter_files,
    generate_documentation,
)
from docalypt.llm import (
    LLMSettings,
    LLMError,
    PROMPT_TEMPLATE,
    list_models,
    settings_from_env,
    resolve_system_prompt,
)

# Load environment on module import
load_env()

# Initialize FastAPI app
app = FastAPI(
    title="Docalypt API",
    description="REST API for Docalypt - Transcript to Documentation Generator",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage for uploaded files and generated content
UPLOAD_DIR = Path(tempfile.gettempdir()) / "docalypt_uploads"
OUTPUT_DIR = Path(tempfile.gettempdir()) / "docalypt_output"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# In-memory session storage
sessions: Dict[str, Dict[str, Any]] = {}


# =============================================================================
# Pydantic Models for Request/Response
# =============================================================================

class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: str
    version: str = "1.0.0"


class SessionResponse(BaseModel):
    session_id: str
    created_at: str
    upload_path: str


class FileUploadResponse(BaseModel):
    session_id: str
    filename: str
    file_path: str
    size_bytes: int


class SplitRequest(BaseModel):
    session_id: str
    marker_regex: Optional[str] = None
    export_html: bool = False
    simple_mode: bool = True  # If True, supports any markdown file (not just transcripts)


class SplitResponse(BaseModel):
    session_id: str
    chapters: List[Dict[str, Any]]
    chapter_count: int
    html_path: Optional[str] = None


class ChapterInfo(BaseModel):
    index: int
    filename: str
    title: str
    preview: str
    path: str


class LLMSettingsRequest(BaseModel):
    provider: str = "ollama"
    model: str = ""
    temperature: float = 0.2
    max_tokens: int = 800
    top_p: float = 0.9
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    repeat_penalty: float = 1.0
    top_k: int = 40
    endpoint: Optional[str] = None
    api_key: Optional[str] = None
    anthropic_version: Optional[str] = None
    system_prompt_text: Optional[str] = None
    system_prompt_allow_empty: bool = False


class DocGenRequest(BaseModel):
    session_id: str
    chapter_indices: Optional[List[int]] = None  # None means all chapters
    settings: LLMSettingsRequest
    prompt_template: Optional[str] = None


class DocGenResponse(BaseModel):
    session_id: str
    generated: List[Dict[str, str]]
    failures: List[Dict[str, str]]
    total_chapters: int
    successful: int
    failed: int


class ModelsResponse(BaseModel):
    provider: str
    models: List[str]


class ProviderStatusResponse(BaseModel):
    provider: str
    available: bool
    message: str
    models_count: int = 0


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check API health status."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/api/sessions", response_model=SessionResponse)
async def create_session():
    """Create a new session for file processing."""
    session_id = str(uuid.uuid4())
    session_path = UPLOAD_DIR / session_id
    session_path.mkdir(parents=True, exist_ok=True)
    
    output_path = OUTPUT_DIR / session_id
    output_path.mkdir(parents=True, exist_ok=True)
    
    sessions[session_id] = {
        "created_at": datetime.utcnow().isoformat(),
        "upload_path": str(session_path),
        "output_path": str(output_path),
        "files": [],
        "chapters": [],
        "documentation": [],
    }
    
    return SessionResponse(
        session_id=session_id,
        created_at=sessions[session_id]["created_at"],
        upload_path=str(session_path),
    )


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session details."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session and cleanup files."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Cleanup files
    session_upload = UPLOAD_DIR / session_id
    session_output = OUTPUT_DIR / session_id
    
    if session_upload.exists():
        shutil.rmtree(session_upload)
    if session_output.exists():
        shutil.rmtree(session_output)
    
    del sessions[session_id]
    return {"message": "Session deleted successfully"}


@app.post("/api/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    session_id: str = Query(...),
):
    """Upload a markdown transcript file."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not file.filename.lower().endswith(".md"):
        raise HTTPException(status_code=400, detail="File must be a Markdown file (.md)")
    
    session_path = Path(sessions[session_id]["upload_path"])
    file_path = session_path / file.filename
    
    # Save the file
    content = await file.read()
    file_path.write_bytes(content)
    
    # Update session
    sessions[session_id]["files"].append({
        "filename": file.filename,
        "path": str(file_path),
        "size_bytes": len(content),
    })
    
    return FileUploadResponse(
        session_id=session_id,
        filename=file.filename,
        file_path=str(file_path),
        size_bytes=len(content),
    )


@app.get("/api/files/{session_id}")
async def list_files(session_id: str):
    """List all uploaded files in a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"files": sessions[session_id]["files"]}


@app.post("/api/split", response_model=SplitResponse)
async def split_transcript(request: SplitRequest):
    """Split a transcript or markdown file into chapters.
    
    If simple_mode is True (default), any markdown file can be processed:
    - Files are split by top-level headings (# or ##)
    - If no headings found, the entire file becomes one chapter
    
    If simple_mode is False, the original transcript format is required:
    - Must have timestamp headers and 'Transcript:' separator
    """
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[request.session_id]
    
    if not session["files"]:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    # Get the first uploaded file
    input_file = Path(session["files"][0]["path"])
    output_dir = Path(session["output_path"]) / "chapters"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Read file content
        content = input_file.read_text(encoding="utf-8")
        
        # Check if it's a proper transcript format
        is_transcript_format = "\n\nTranscript:" in content
        
        if not request.simple_mode and not is_transcript_format:
            raise HTTPException(
                status_code=400, 
                detail="Transcript missing 'Transcript:' separator. Enable simple_mode for regular markdown files."
            )
        
        chapters = []
        
        if is_transcript_format and not request.simple_mode:
            # Use original TranscriptSplitter for proper transcripts
            splitter = TranscriptSplitter(
                input_path=input_file,
                output_dir=output_dir,
                marker_regex=request.marker_regex,
            )
            result = splitter._split_internal(export_html=request.export_html)
            
            for idx, chapter_path in enumerate(result.chapters):
                chapter_content = chapter_path.read_text(encoding="utf-8")
                lines = chapter_content.strip().split("\n")
                title = lines[0].lstrip("# ").strip() if lines else chapter_path.stem
                preview = "\n".join(lines[:5]) if len(lines) > 5 else chapter_content
                
                chapters.append({
                    "index": idx,
                    "filename": chapter_path.name,
                    "title": title,
                    "preview": preview[:500],
                    "path": str(chapter_path),
                })
        else:
            # Simple mode: split by headings or use as single chapter
            import re
            
            chapters = []
            
            # First, check for timestamp-based chapter headers (transcript format)
            # Format: HH:MM:SS - Title OR HH:MM:SS – Title (with dash or en-dash)
            timestamp_pattern = re.compile(r'^(\d{2}:\d{2}:\d{2})\s*[-–]\s*(.+)$', re.MULTILINE)
            timestamp_matches = list(timestamp_pattern.finditer(content))
            
            if len(timestamp_matches) >= 2:
                # This looks like a transcript with multiple chapter headers
                # Extract the header section (before "Transcript:" if present)
                transcript_marker = content.find("\n\nTranscript:")
                if transcript_marker == -1:
                    transcript_marker = content.find("\nTranscript:")
                
                if transcript_marker != -1:
                    header_section = content[:transcript_marker]
                    body = content[transcript_marker:].split(":", 1)[1] if ":" in content[transcript_marker:] else ""
                else:
                    header_section = content
                    body = ""
                
                header_matches = list(timestamp_pattern.finditer(header_section))
                
                if header_matches and body:
                    # Build a map of timestamps to find content in body
                    # Body timestamps are like (00:00) or (03:42) - minutes:seconds format
                    body_timestamp_pattern = re.compile(r'\((\d{2}:\d{2})\)')
                    
                    # Convert header timestamps HH:MM:SS to MM:SS for matching
                    def hms_to_ms(hms):
                        """Convert HH:MM:SS to total minutes for comparison"""
                        parts = hms.split(":")
                        return int(parts[0]) * 60 + int(parts[1])
                    
                    def ms_to_minutes(ms):
                        """Convert MM:SS string to total minutes"""
                        parts = ms.split(":")
                        return int(parts[0])
                    
                    # Find all body timestamps and their positions
                    body_timestamps = [(m.group(1), m.start(), m.end()) for m in body_timestamp_pattern.finditer(body)]
                    
                    for idx, match in enumerate(header_matches):
                        timestamp = match.group(1)  # HH:MM:SS
                        title = match.group(2).strip()
                        
                        # Remove leading number from title for cleaner filename
                        # e.g., "1. Overview of the IoT PCB Design" -> "Overview of the IoT PCB Design"
                        clean_title = re.sub(r'^\d+\.\s*', '', title)
                        
                        # Create safe filename without redundant numbering
                        safe_title = re.sub(r'[^\w\s-]', '', clean_title).strip()
                        safe_title = re.sub(r'[-\s]+', '_', safe_title).lower()[:50]
                        filename = f"{idx + 1:02d}_{safe_title}.md"
                        
                        # Extract content from body for this chapter
                        chapter_minutes = hms_to_ms(timestamp)
                        
                        # Find the starting position in body for this timestamp
                        start_pos = 0
                        for bt, bt_start, bt_end in body_timestamps:
                            bt_mins = ms_to_minutes(bt)
                            if bt_mins >= chapter_minutes:
                                start_pos = bt_start
                                break
                        
                        # Find the ending position (start of next chapter)
                        end_pos = len(body)
                        if idx + 1 < len(header_matches):
                            next_timestamp = header_matches[idx + 1].group(1)
                            next_minutes = hms_to_ms(next_timestamp)
                            for bt, bt_start, bt_end in body_timestamps:
                                bt_mins = ms_to_minutes(bt)
                                if bt_mins >= next_minutes:
                                    end_pos = bt_start
                                    break
                        
                        # Extract chapter content
                        chapter_body = body[start_pos:end_pos].strip()
                        
                        # Clean up the content - remove timestamp markers like (00:00)
                        chapter_body = re.sub(r'\(\d{2}:\d{2}\)\s*', '', chapter_body)
                        
                        # Build full chapter content
                        chapter_content = f"# {title}\n\n{chapter_body}\n"
                        
                        chapter_path = output_dir / filename
                        chapter_path.write_text(chapter_content, encoding="utf-8")
                        
                        lines = chapter_content.split("\n")
                        preview = "\n".join(lines[:5]) if len(lines) > 5 else chapter_content
                        
                        chapters.append({
                            "index": idx,
                            "filename": filename,
                            "title": title,
                            "preview": preview[:500],
                            "path": str(chapter_path),
                        })
            
            # If no timestamp headers found, try markdown headings
            if not chapters:
                # Find all level 1 and 2 headings
                heading_pattern = re.compile(r'^(#{1,2})\s+(.+)$', re.MULTILINE)
                matches = list(heading_pattern.finditer(content))
                
                if matches:
                    # Split by headings
                    for idx, match in enumerate(matches):
                        start = match.start()
                        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
                        
                        chapter_content = content[start:end].strip()
                        title = match.group(2).strip()
                        
                        # Create safe filename
                        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
                        safe_title = re.sub(r'[-\s]+', '_', safe_title).lower()[:40]
                        filename = f"{idx + 1:02d}_{safe_title}.md"
                        
                        chapter_path = output_dir / filename
                        chapter_path.write_text(chapter_content, encoding="utf-8")
                        
                        lines = chapter_content.split("\n")
                        preview = "\n".join(lines[:5]) if len(lines) > 5 else chapter_content
                        
                        chapters.append({
                            "index": idx,
                            "filename": filename,
                            "title": title,
                            "preview": preview[:500],
                            "path": str(chapter_path),
                        })
            
            # If still no chapters, treat entire file as one chapter
            if not chapters:
                title = input_file.stem.replace('_', ' ').replace('-', ' ').title()
                filename = f"01_{input_file.stem}.md"
                
                chapter_path = output_dir / filename
                chapter_path.write_text(content, encoding="utf-8")
                
                lines = content.split("\n")
                preview = "\n".join(lines[:5]) if len(lines) > 5 else content
                
                chapters.append({
                    "index": 0,
                    "filename": filename,
                    "title": title,
                    "preview": preview[:500],
                    "path": str(chapter_path),
                })

        
        # Update session
        session["chapters"] = chapters
        
        return SplitResponse(
            session_id=request.session_id,
            chapters=chapters,
            chapter_count=len(chapters),
            html_path=None,
        )
    
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Split failed: {str(exc)}")


@app.get("/api/chapters/{session_id}")
async def get_chapters(session_id: str):
    """Get all chapters for a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"chapters": sessions[session_id]["chapters"]}


@app.get("/api/chapters/{session_id}/{index}")
async def get_chapter_content(session_id: str, index: int):
    """Get full content of a specific chapter."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chapters = sessions[session_id]["chapters"]
    if index < 0 or index >= len(chapters):
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter = chapters[index]
    content = Path(chapter["path"]).read_text(encoding="utf-8")
    
    return {
        **chapter,
        "content": content,
    }


@app.get("/api/models", response_model=ModelsResponse)
async def get_models(
    provider: str = Query("ollama"),
    endpoint: Optional[str] = Query(None),
    api_key: Optional[str] = Query(None),
):
    """List available models for a provider."""
    settings = LLMSettings(
        provider=provider,
        endpoint=endpoint,
        api_key=api_key,
    )
    
    try:
        models = list_models(settings)
        return ModelsResponse(provider=provider, models=models)
    except LLMError as exc:
        raise HTTPException(status_code=503, detail=str(exc))


@app.get("/api/providers/status", response_model=List[ProviderStatusResponse])
async def check_providers():
    """Check status of all configured LLM providers."""
    results = []
    
    # Check Ollama
    try:
        settings = LLMSettings(provider="ollama")
        models = list_models(settings)
        results.append(ProviderStatusResponse(
            provider="ollama",
            available=True,
            message="Connected",
            models_count=len(models),
        ))
    except Exception as exc:
        results.append(ProviderStatusResponse(
            provider="ollama",
            available=False,
            message=str(exc),
        ))
    
    # Check OpenAI (if API key configured)
    openai_key = os.getenv("DOCALYPT_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            settings = LLMSettings(provider="openai", api_key=openai_key)
            models = list_models(settings)
            results.append(ProviderStatusResponse(
                provider="openai",
                available=True,
                message="Connected",
                models_count=len(models),
            ))
        except Exception as exc:
            results.append(ProviderStatusResponse(
                provider="openai",
                available=False,
                message=str(exc),
            ))
    else:
        results.append(ProviderStatusResponse(
            provider="openai",
            available=False,
            message="API key not configured",
        ))
    
    # Anthropic status
    anthropic_key = os.getenv("DOCALYPT_ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        results.append(ProviderStatusResponse(
            provider="anthropic",
            available=True,
            message="API key configured (model list not available)",
        ))
    else:
        results.append(ProviderStatusResponse(
            provider="anthropic",
            available=False,
            message="API key not configured",
        ))
    
    return results


@app.post("/api/docgen", response_model=DocGenResponse)
async def generate_docs(request: DocGenRequest):
    """Generate documentation for chapters using LLM."""
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[request.session_id]
    
    if not session["chapters"]:
        raise HTTPException(status_code=400, detail="No chapters available. Run split first.")
    
    # Determine which chapters to process
    all_chapters = session["chapters"]
    if request.chapter_indices:
        chapter_paths = [
            Path(all_chapters[i]["path"])
            for i in request.chapter_indices
            if 0 <= i < len(all_chapters)
        ]
    else:
        chapter_paths = [Path(ch["path"]) for ch in all_chapters]
    
    if not chapter_paths:
        raise HTTPException(status_code=400, detail="No valid chapters selected")
    
    # Build LLM settings
    settings = LLMSettings(
        provider=request.settings.provider,
        model=request.settings.model,
        temperature=request.settings.temperature,
        max_tokens=request.settings.max_tokens,
        top_p=request.settings.top_p,
        presence_penalty=request.settings.presence_penalty,
        frequency_penalty=request.settings.frequency_penalty,
        repeat_penalty=request.settings.repeat_penalty,
        top_k=request.settings.top_k,
        endpoint=request.settings.endpoint,
        api_key=request.settings.api_key,
        anthropic_version=request.settings.anthropic_version,
        system_prompt_text=request.settings.system_prompt_text,
        system_prompt_allow_empty=request.settings.system_prompt_allow_empty,
    )
    
    # Create request
    doc_request = DocumentGenerationRequest(
        chapters=chapter_paths,
        settings=settings,
        prompt_template=request.prompt_template or PROMPT_TEMPLATE,
    )
    
    try:
        result = generate_documentation(doc_request)
        
        generated = [
            {"chapter": str(ch.name), "documentation": str(doc.name)}
            for ch, doc in result.written
        ]
        failures = [
            {"chapter": str(ch.name), "error": error}
            for ch, error in result.failures
        ]
        
        # Update session with documentation info
        session["documentation"] = generated
        
        return DocGenResponse(
            session_id=request.session_id,
            generated=generated,
            failures=failures,
            total_chapters=len(chapter_paths),
            successful=len(result.written),
            failed=len(result.failures),
        )
    
    except LLMError as exc:
        raise HTTPException(status_code=503, detail=f"LLM error: {str(exc)}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(exc)}")


@app.get("/api/docgen/stream/{session_id}")
async def stream_docgen(
    session_id: str,
    provider: str = Query("ollama"),
    model: str = Query(...),
    chapter_indices: str = Query(None),
):
    """Stream documentation generation progress via Server-Sent Events."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    if not session["chapters"]:
        raise HTTPException(status_code=400, detail="No chapters available")
    
    async def event_stream() -> AsyncGenerator[str, None]:
        all_chapters = session["chapters"]
        
        # Parse chapter indices
        indices = None
        if chapter_indices:
            indices = [int(i) for i in chapter_indices.split(",")]
        
        chapter_paths = (
            [Path(all_chapters[i]["path"]) for i in indices]
            if indices
            else [Path(ch["path"]) for ch in all_chapters]
        )
        
        settings = LLMSettings(provider=provider, model=model)
        
        total = len(chapter_paths)
        for idx, chapter_path in enumerate(chapter_paths):
            yield f"data: {json.dumps({'type': 'progress', 'current': idx + 1, 'total': total, 'chapter': chapter_path.name})}\n\n"
            
            try:
                doc_request = DocumentGenerationRequest(
                    chapters=[chapter_path],
                    settings=settings,
                )
                result = generate_documentation(doc_request)
                
                if result.written:
                    yield f"data: {json.dumps({'type': 'success', 'chapter': chapter_path.name, 'doc': str(result.written[0][1].name)})}\n\n"
                elif result.failures:
                    yield f"data: {json.dumps({'type': 'error', 'chapter': chapter_path.name, 'error': result.failures[0][1]})}\n\n"
            
            except Exception as exc:
                yield f"data: {json.dumps({'type': 'error', 'chapter': chapter_path.name, 'error': str(exc)})}\n\n"
            
            # Small delay to allow client to process
            await asyncio.sleep(0.1)
        
        yield f"data: {json.dumps({'type': 'complete', 'total': total})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/api/documentation/{session_id}")
async def get_documentation(session_id: str):
    """Get all generated documentation for a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    doc_dir = Path(session["output_path"]) / "chapters" / "documentation"
    
    if not doc_dir.exists():
        return {"documentation": []}
    
    docs = []
    for doc_file in sorted(doc_dir.glob("*.docs.md")):
        content = doc_file.read_text(encoding="utf-8")
        docs.append({
            "filename": doc_file.name,
            "path": str(doc_file),
            "content": content,
            "size_bytes": len(content.encode("utf-8")),
        })
    
    return {"documentation": docs}


@app.get("/api/download/{session_id}")
async def download_all(session_id: str):
    """Download all generated content as a ZIP file."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    output_path = Path(session["output_path"])
    
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="No output available")
    
    zip_path = output_path.parent / f"{session_id}.zip"
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", output_path)
    
    return FileResponse(
        path=str(zip_path),
        filename=f"docalypt_export_{session_id[:8]}.zip",
        media_type="application/zip",
    )


@app.get("/api/settings/default")
async def get_default_settings():
    """Get default LLM settings from environment."""
    settings = settings_from_env()
    
    return {
        "provider": settings.provider,
        "model": settings.model,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
        "top_p": settings.top_p,
        "presence_penalty": settings.presence_penalty,
        "frequency_penalty": settings.frequency_penalty,
        "repeat_penalty": settings.repeat_penalty,
        "top_k": settings.top_k,
        "endpoint": settings.resolved_endpoint(),
        "prompt_template": PROMPT_TEMPLATE,
    }


# =============================================================================
# Static Files (Frontend)
# =============================================================================

# Mount static files last to not override API routes
frontend_path = Path(__file__).parent / "static"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")


def run_server(host: str = "127.0.0.1", port: int = 8000):
    """Run the development server."""
    import uvicorn
    uvicorn.run(app, host=host, port=port, reload=True)


if __name__ == "__main__":
    run_server()

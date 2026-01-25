import os
import logging
from typing import List, Optional
from pathlib import Path
import asyncio
import psutil
import subprocess
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import shutil

from docalypt.env import load_env
from docalypt.llm import list_models, settings_from_env, LLMSettings, resolve_system_prompt
from docalypt.documentation import (
    generate_documentation,
    DocumentGenerationRequest,
    PROMPT_TEMPLATE,
)
from docalypt.splitting import TranscriptSplitter
from docalypt.heading_splitting import split_by_headings

# Load environment variables
load_env()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("docalypt.server")

app = FastAPI(title="Docalypt API")

# --- System Monitoring ---

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # Broadcast to all connected clients
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.active_connections.remove(connection)

manager = ConnectionManager()

def get_gpu_usage():
    try:
        # Simple nvidia-smi check for Windows/Linux
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False
        )
        if result.returncode == 0:
            output = result.stdout.decode('utf-8').strip()
            if output:
                return float(output.split('\n')[0])
    except Exception:
        pass
    return None

def check_ollama():
    try:
        # Ollama usually runs on 11434
        response = requests.get("http://localhost:11434/", timeout=0.5)
        return response.status_code == 200
    except Exception:
        return False

async def system_monitor_loop():
    while True:
        try:
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent
            gpu = get_gpu_usage()
            ollama_status = await run_in_threadpool(check_ollama)
            
            await manager.broadcast({
                "type": "system_stats",
                "data": {
                    "cpu": cpu,
                    "ram": ram,
                    "gpu": gpu if gpu is not None else 0,
                    "has_gpu": gpu is not None,
                    "ollama": ollama_status
                }
            })
        except Exception as e:
            logger.error(f"Monitor error: {e}")
        
        await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(system_monitor_loop())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- End System Monitoring ---

# Paths & configuration
BASE_DIR = Path(__file__).resolve().parent
ENV_TRANSCRIPTS_DIR = "DOCALYPT_TRANSCRIPTS_DIR"
ENV_GENERATED_DIR = "DOCALYPT_GENERATED_DIR"
ENV_PROMPTS_DIR = "DOCALYPT_PROMPTS_DIR"
ENV_CORS_ORIGINS = "DOCALYPT_CORS_ORIGINS"

DEFAULT_TRANSCRIPTS_DIRNAME = "transcripts"
DEFAULT_GENERATED_DIRNAME = "generated"
DEFAULT_PROMPTS_DIRNAME = "prompts"

DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"


def _is_testing() -> bool:
    return bool(os.getenv("PYTEST_CURRENT_TEST")) or os.getenv("DOCALYPT_TESTING") == "true"


def _parse_origins(value: Optional[str]) -> List[str]:
    raw = (value or DEFAULT_CORS_ORIGINS).strip()
    if raw == "*":
        return ["*"]
    origins = [item.strip() for item in raw.split(",") if item.strip()]
    return origins or ["*"]


def _resolve_dir(env_var: str, default_name: str) -> Path:
    raw = os.getenv(env_var)
    if raw:
        path = Path(raw).expanduser()
    else:
        path = BASE_DIR / default_name
    path = path.resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def _safe_relative_path(value: str, *, allow_subdirs: bool) -> Path:
    cleaned = value.replace("\\", "/").strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Path missing")
    candidate = Path(cleaned)
    if candidate.is_absolute() or candidate.drive or candidate.anchor or ".." in candidate.parts:
        raise HTTPException(status_code=400, detail="Invalid path")
    if not allow_subdirs and len(candidate.parts) > 1:
        raise HTTPException(status_code=400, detail="Subdirectories are not allowed")
    return candidate


def _safe_join(base: Path, value: str, *, allow_subdirs: bool) -> Path:
    rel_path = _safe_relative_path(value, allow_subdirs=allow_subdirs)
    combined = (base / rel_path).resolve()
    if not _is_relative_to(combined, base):
        raise HTTPException(status_code=400, detail="Invalid path")
    return combined


def _transcripts_dir() -> Path:
    return _resolve_dir(ENV_TRANSCRIPTS_DIR, DEFAULT_TRANSCRIPTS_DIRNAME)


def _generated_dir() -> Path:
    return _resolve_dir(ENV_GENERATED_DIR, DEFAULT_GENERATED_DIRNAME)


def _prompts_dir() -> Path:
    return _resolve_dir(ENV_PROMPTS_DIR, DEFAULT_PROMPTS_DIRNAME)


# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_origins(os.getenv(ENV_CORS_ORIGINS)),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class ConfigUpdate(BaseModel):
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=32768)
    presence_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0)
    frequency_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0)
    repeat_penalty: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_k: Optional[int] = Field(None, ge=1, le=1000)
    system_prompt: Optional[str] = None
    prompt_template: Optional[str] = None

class GenerationRequest(BaseModel):
    files: List[str]
    standalone: Optional[bool] = False

class GenerationPayload(BaseModel):
    req: GenerationRequest
    config: ConfigUpdate = Field(default_factory=ConfigUpdate)

# Ensure directories exist
_transcripts_dir()
_generated_dir()
_prompts_dir()

# --- Endpoints ---

@app.get("/api/config")
def get_config():
    """Get current configuration and available models."""
    settings = settings_from_env()
    system_prompt_text = settings.system_prompt_text or ""
    return {
        "provider": settings.provider,
        "model": settings.model,
        "temperature": settings.temperature,
        "top_p": settings.top_p,
        "max_tokens": settings.max_tokens,
        "presence_penalty": settings.presence_penalty,
        "frequency_penalty": settings.frequency_penalty,
        "repeat_penalty": settings.repeat_penalty,
        "top_k": settings.top_k,
        "system_prompt": system_prompt_text,
        "prompt_template": PROMPT_TEMPLATE,
        "system_prompt_wrapper": resolve_system_prompt(LLMSettings()),
    }

@app.get("/api/models")
def get_models(provider: str = "ollama"):
    """List available models for the provider."""
    current_settings = settings_from_env()
    current_settings.provider = provider
    
    try:
        models = list_models(current_settings)
        return {"models": models}
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/files")
def list_files():
    """List all available markdown transcript files recursively."""
    transcripts_dir = _transcripts_dir()
    files = []
    if transcripts_dir.exists():
        # rglob to find files in subdirectories (chapters)
        for f in transcripts_dir.rglob("*.md"):
            if not f.name.endswith(".docs.md"):
                # Use as_posix for frontend compatibility
                rel_path = f.relative_to(transcripts_dir).as_posix()
                files.append({
                    "name": f.name, 
                    "path": rel_path,
                    "size": f.stat().st_size
                })
    return {"files": files}

@app.post("/api/open-folder")
async def open_folder(payload: dict):
    """Open a folder in the system file explorer."""
    import subprocess
    import platform

    folder_type = payload.get("type", "transcripts")  # "transcripts" or "generated"
    if folder_type == "transcripts":
        folder_path = _transcripts_dir()
    elif folder_type == "generated":
        folder_path = _generated_dir()
    else:
        raise HTTPException(status_code=400, detail="Unsupported folder type")
    
    folder_path.mkdir(exist_ok=True)
    abs_path = folder_path.resolve()
    
    if _is_testing():
        return {"status": "success", "path": str(abs_path), "skipped": True}

    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(str(abs_path))  # type: ignore[attr-defined]
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(abs_path)], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", str(abs_path)], check=True)

        return {"status": "success", "path": str(abs_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open folder: {e}")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a new transcript file."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files are allowed")

    transcripts_dir = _transcripts_dir()
    safe_name = _safe_relative_path(file.filename, allow_subdirs=False).name
    file_path = transcripts_dir / safe_name
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
        
    return {"filename": file.filename, "status": "uploaded"}

@app.get("/api/prompts")
def list_prompts():
    """List available prompt templates from the prompts directory."""
    prompts_dir = _prompts_dir()
    prompts = []
    if prompts_dir.exists():
        for f in prompts_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            title = f.stem
            description = "Custom prompt template."
            lines = content.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    description = line.strip()
                    break
            
            prompts.append({
                "name": f.name,
                "title": title.replace('_', ' ').title(),
                "description": description[:100] + ("..." if len(description) > 100 else "")
            })
    return {"prompts": prompts}

@app.get("/api/prompts/{name}")
def get_prompt_content(name: str):
    """Get the full content of a specific prompt template."""
    prompts_dir = _prompts_dir()
    safe_name = _safe_relative_path(name, allow_subdirs=False).name
    if not safe_name.endswith(".md"):
        raise HTTPException(status_code=400, detail="Invalid prompt name")
    path = prompts_dir / safe_name
    if not path.exists():
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"name": name, "content": path.read_text(encoding="utf-8")}

@app.post("/api/split")
async def split_file(payload: dict):
    """Split a transcript file into chapters."""
    filename = payload.get("filename")
    if not filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    transcripts_dir = _transcripts_dir()
    file_path = _safe_join(transcripts_dir, filename, allow_subdirs=True)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
        
    output_dir = transcripts_dir / file_path.stem
    
    # Try TranscriptSplitter first if "Transcript:" exists
    content = file_path.read_text(encoding="utf-8")
    if "Transcript:" in content:
        try:
            splitter = TranscriptSplitter(input_path=file_path, output_dir=output_dir)
            splitter.split()
            # Convert SplitResult paths to our format
            chapters = []
            for i, p in enumerate(sorted(output_dir.glob("*.md")), 1):
                if not p.name.endswith(".docs.md"):
                    # We need a title. TranscriptSplitter title is usually first line # Title
                    first_line = p.read_text().splitlines()[0]
                    title = first_line.lstrip('#').strip()
                    chapters.append({
                        "id": i,
                        "title": title,
                        "filename": p.name,
                        "path": p.relative_to(transcripts_dir).as_posix()
                    })
            return {"chapters": chapters}
        except Exception as e:
            logger.warning(f"TranscriptSplitter failed, falling back to headings: {e}")
            
    # Fallback/Default to Heading Splitter
    try:
        chapters = split_by_headings(file_path, output_dir, base_dir=transcripts_dir)
        # Add ID for frontend
        for i, c in enumerate(chapters, 1):
            c["id"] = i
        return {"chapters": chapters}
    except Exception as e:
        logger.error(f"Splitting failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def generate_docs(payload: GenerationPayload):
    """Generate documentation for selected files."""

    req = payload.req
    config = payload.config

    transcripts_dir = _transcripts_dir()
    selected_files = []
    for filename in req.files:
        try:
            path = _safe_join(transcripts_dir, filename, allow_subdirs=True)
        except HTTPException:
            continue
        if path.exists() and path.is_file():
            selected_files.append(path)
    
    if not selected_files:
        raise HTTPException(status_code=400, detail="No valid files selected")
    
    # Merge with defaults
    defaults = settings_from_env()
    
    settings = LLMSettings(
        provider=config.provider or defaults.provider,
        model=config.model or defaults.model,
        temperature=config.temperature if config.temperature is not None else defaults.temperature,
        top_p=config.top_p if config.top_p is not None else defaults.top_p,
        max_tokens=config.max_tokens or defaults.max_tokens,
        presence_penalty=config.presence_penalty if config.presence_penalty is not None else defaults.presence_penalty,
        frequency_penalty=config.frequency_penalty if config.frequency_penalty is not None else defaults.frequency_penalty,
        repeat_penalty=config.repeat_penalty if config.repeat_penalty is not None else defaults.repeat_penalty,
        top_k=config.top_k or defaults.top_k,
        system_prompt_text=config.system_prompt if config.system_prompt is not None else defaults.system_prompt_text,
        system_prompt_allow_empty=config.system_prompt is not None
    )
    
    generated_root = _generated_dir()

    # Create a progress callback that broadcasts to WebSocket
    def report_progress(current: int, total: int, filename: str):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
            
        # We need the loop that the server is running on
        # Since we are inside an async endpoint, asyncio.get_running_loop() works here
        # BUT this callback is called from a thread, so we can't get the loop from *there* easily
        # unless we capture it from the parent scope.
        pass

    # Capture the current event loop for threadsafe execution
    loop = asyncio.get_running_loop()

    def progress_callback(current: int, total: int, filename: str):
        asyncio.run_coroutine_threadsafe(
            manager.broadcast({
                "type": "generation_progress",
                "data": {
                    "current": current,
                    "total": total,
                    "filename": filename,
                    "percent": int((current / total) * 100) if total > 0 else 0
                }
            }),
            loop
        )

    try:
        gen_request = DocumentGenerationRequest(
            chapters=selected_files,
            settings=settings,
            prompt_template=config.prompt_template or PROMPT_TEMPLATE,
            destination_root=generated_root,
            source_root=transcripts_dir,
            standalone=req.standalone,
            progress_callback=progress_callback
        )
        
        result = await run_in_threadpool(generate_documentation, gen_request)
        
        # Send completion value (100%)
        await manager.broadcast({
            "type": "generation_progress",
            "data": {
                "current": len(selected_files),
                "total": len(selected_files),
                "filename": "Done",
                "percent": 100,
                "done": True
            }
        })
        
        if req.standalone:
            successes = [f"Standalone Report -> {result.written[0][1].name}"] if result.written else []
        else:
            successes = [f"{c.name} -> {d.name}" for c, d in result.written]
            
        failures = [f"{str(c)}: {e}" for c, e in result.failures]
        
        return {
            "status": "completed", 
            "generated": successes, 
            "failed": failures,
            "success": len(failures) == 0
        }

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/files")
async def delete_files(payload: dict):
    """Delete selected files or directories from transcripts."""
    files_to_delete = payload.get("files", [])
    if not files_to_delete:
        raise HTTPException(status_code=400, detail="No files specified")
    
    deleted = []
    failed = []

    transcripts_dir = _transcripts_dir()
    for file_path in files_to_delete:
        try:
            # Normalize path
            clean_path = file_path.replace("\\", "/").replace("transcripts/", "")
            full_path = _safe_join(transcripts_dir, clean_path, allow_subdirs=True)
            
            if full_path.exists():
                if full_path.is_file():
                    full_path.unlink()
                    deleted.append(file_path)
                elif full_path.is_dir():
                    shutil.rmtree(full_path)
                    deleted.append(file_path)
            else:
                failed.append(f"{file_path}: Not found")
        except HTTPException as exc:
            failed.append(f"{file_path}: {exc.detail}")
        except Exception as e:
            failed.append(f"{file_path}: {str(e)}")
    
    return {
        "deleted": deleted,
        "failed": failed,
        "status": "completed"
    }

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

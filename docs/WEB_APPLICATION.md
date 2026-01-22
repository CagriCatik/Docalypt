# Docalypt Web Application

This document describes the web application migration of Docalypt - transforming the desktop PySide6 GUI into a modern browser-based application.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Web Browser                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Frontend (HTML/JS/CSS)                  │  │
│  │  - Responsive SPA-like Interface                          │  │
│  │  - Real-time Progress Updates                              │  │
│  │  - LLM Settings Configuration                             │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│  │ /api/split   │ │ /api/docgen  │ │ /api/models              │ │
│  │ /api/chapters│ │ /api/settings│ │ /api/health              │ │
│  └──────────────┘ └──────────────┘ └──────────────────────────┘ │
│                                                                  │
│  Core Modules (Existing):                                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│  │ splitting.py │ │documentation │ │       llm.py             │ │
│  │              │ │    .py       │ │  (Ollama/OpenAI/Claude)  │ │
│  └──────────────┘ └──────────────┘ └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web Application

```bash
python run_web.py
```

The application will be available at:
- **Web UI**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/api/docs
- **ReDoc**: http://127.0.0.1:8000/api/redoc

### 3. Command-line Options

```bash
python run_web.py --host 0.0.0.0 --port 3000  # Custom port, expose to network
python run_web.py --no-reload                  # Disable auto-reload
```

## Features

### Frontend (HTML/CSS/JavaScript)

- **Modern Dark Theme**: Glassmorphism effects with animated gradients
- **Responsive Design**: Works on desktop and tablet
- **Drag & Drop Upload**: Easy file upload for Markdown files
- **Visual Workflow**: 4-step progress indicator (Upload → Split → Generate → Export)
- **Real-time Updates**: Progress bars and toast notifications
- **Chapter Preview**: View generated documentation inline
- **Settings Persistence**: Local storage for API keys and preferences

### Backend (FastAPI)

- **RESTful API**: Clean, documented endpoints
- **Session Management**: Isolated file processing per session
- **Flexible Splitting**: 
  - Simple mode: Split any Markdown by headings
  - Transcript mode: Original format with timestamp markers
- **LLM Integration**: Support for Ollama, OpenAI, and Anthropic
- **Streaming Support**: Server-Sent Events for real-time progress
- **Export**: Download all generated content as ZIP

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/sessions` | POST | Create new session |
| `/api/sessions/{id}` | GET/DELETE | Get or delete session |
| `/api/upload` | POST | Upload Markdown file |
| `/api/split` | POST | Split into chapters |
| `/api/chapters/{id}` | GET | List chapters |
| `/api/chapters/{id}/{idx}` | GET | Get chapter content |
| `/api/models` | GET | List available models |
| `/api/providers/status` | GET | Check LLM providers |
| `/api/docgen` | POST | Generate documentation |
| `/api/documentation/{id}` | GET | Get generated docs |
| `/api/download/{id}` | GET | Download as ZIP |

## File Structure

```
web/
├── __init__.py          # Package init
├── api.py               # FastAPI backend with all endpoints
└── static/
    ├── index.html       # Main HTML with Tailwind CSS
    ├── styles.css       # Custom CSS (glassmorphism, animations)
    ├── app.js           # Frontend JavaScript application
    └── favicon.svg      # SVG favicon

tests/
├── test_web_api.py      # Backend API tests (41 tests)
└── test_frontend.js     # Frontend JavaScript tests
```

## Running Tests

### Backend Tests

```bash
python -m pytest tests/test_web_api.py -v
```

### Frontend Tests

Open the browser console when running the app and load `test_frontend.js`, or run with Node.js:

```bash
node tests/test_frontend.js
```

## Configuration

### Environment Variables

The web app uses the same `.env` configuration as the CLI/GUI:

```env
DOCALYPT_LLM_PROVIDER=ollama
DOCALYPT_LLM_MODEL=llama3
DOCALYPT_LLM_ENDPOINT=http://localhost:11434

# Optional: API keys for cloud providers
DOCALYPT_OPENAI_API_KEY=sk-...
DOCALYPT_ANTHROPIC_API_KEY=sk-ant-...
```

### Browser Settings

API keys and endpoint can also be configured in the UI via the Settings modal. These are stored in browser localStorage.

## Workflow

1. **Upload**: Drop a Markdown file onto the upload zone
2. **Split**: Click "Split into Chapters" to parse the document
   - Files with headings (# or ##) are split at each heading
   - Files without headings become a single chapter
3. **Configure LLM**: Select provider and model
4. **Generate**: Click "Generate Documentation" for selected chapters
5. **Export**: Download all content as a ZIP file

## Development

### Hot Reload

The development server uses uvicorn with hot reload enabled:

```bash
python run_web.py  # Auto-reload on file changes
```

### Tailwind CSS

Currently using Tailwind CDN for development. For production:

```bash
npm install -D tailwindcss
npx tailwindcss init
npx tailwindcss -i ./web/static/styles.css -o ./web/static/output.css --watch
```

## Migration Notes

### From Desktop GUI

| Desktop Feature | Web Equivalent |
|-----------------|----------------|
| File dialog | Drag & drop upload zone |
| Progress callbacks | Real-time toast notifications |
| Model dropdown | API-populated dropdown with refresh |
| Generation status | Progress bar + SSE updates |
| Save to disk | Download as ZIP export |

### Shared Code

The web app reuses the core modules:
- `docalypt/splitting.py` - Transcript splitting logic
- `docalypt/documentation.py` - Documentation generation
- `docalypt/llm.py` - LLM client implementations
- `docalypt/config.py` - Configuration management

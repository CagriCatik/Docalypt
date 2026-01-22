#!/usr/bin/env python
"""Entry point for the Docalypt web application.

Usage:
    python run_web.py              # Start development server
    python run_web.py --port 3000  # Start on custom port
    python run_web.py --host 0.0.0.0  # Expose to network
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    parser = argparse.ArgumentParser(description="Run Docalypt Web Application")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=True,
        help="Enable auto-reload for development",
    )
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload",
    )
    args = parser.parse_args()

    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn not installed. Run: pip install uvicorn[standard]")
        sys.exit(1)

    # Load environment variables
    from docalypt.env import load_env
    load_env()

    reload = args.reload and not args.no_reload
    
    print("\n" + "=" * 60)
    print(" 🚀 Docalypt Web Application")
    print("=" * 60)
    print(f"\n 📍 Server: http://{args.host}:{args.port}")
    print(f" 📚 API Docs: http://{args.host}:{args.port}/api/docs")
    print(f" 🔄 Auto-reload: {'Enabled' if reload else 'Disabled'}")
    print("\n" + "=" * 60 + "\n")

    uvicorn.run(
        "web.api:app",
        host=args.host,
        port=args.port,
        reload=reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()

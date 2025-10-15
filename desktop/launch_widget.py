"""Launch the Pomodoro & tasks widget in a native window."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import requests
import webview

ROOT_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIST = ROOT_DIR / "frontend" / "dist"
BACKEND_DIR = ROOT_DIR / "backend"


def wait_for_backend(url: str, timeout: float = 15.0) -> None:
    """Poll the backend until it responds or raise after timeout."""

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            response = requests.get(url, timeout=1)
            if response.ok:
                return
        except requests.RequestException:
            time.sleep(0.3)
    raise RuntimeError("Backend did not become ready in time.")


def main() -> None:
    if not FRONTEND_DIST.exists():
        raise SystemExit(
            "Missing frontend build. Run 'npm install && npm run build' inside the 'frontend' "
            "folder before launching the desktop widget."
        )

    backend_proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        cwd=BACKEND_DIR,
    )

    try:
        wait_for_backend("http://127.0.0.1:8000/pomodoro")
        window = webview.create_window(
            "Focus Widget",
            url="http://127.0.0.1:8000/app",
            width=420,
            height=640,
            resizable=False,
            background_color="#f1f5f9",
        )
        webview.start()
    finally:
        backend_proc.terminate()
        try:
            backend_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_proc.kill()


if __name__ == "__main__":
    main()

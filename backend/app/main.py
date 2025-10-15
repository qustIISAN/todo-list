"""FastAPI entrypoint for the desktop widget backend."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_404_NOT_FOUND

from .models import (
    PomodoroResponse,
    PomodoroSettings,
    PomodoroStartRequest,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    TasksResponse,
)
from .services import PomodoroService, TaskService

app = FastAPI(title="Todo & Pomodoro Widget API", version="0.1.0")

# Allow the front-end dev server to communicate with the API during prototyping.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

task_service = TaskService()
pomodoro_service = PomodoroService()


DIST_DIR = Path(__file__).resolve().parents[2] / "frontend" / "dist"

if DIST_DIR.exists():
    app.mount("/app", StaticFiles(directory=DIST_DIR, html=True), name="frontend")

    @app.get("/", include_in_schema=False)
    async def frontend_root() -> RedirectResponse:
        return RedirectResponse(url="/app", status_code=307)


@app.get("/tasks", response_model=TasksResponse)
def list_tasks() -> TasksResponse:
    return task_service.list_tasks()


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreate) -> TaskResponse:
    return task_service.create_task(payload)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    try:
        return task_service.update_task(UUID(task_id), payload)
    except KeyError as exc:  # pragma: no cover - demo error mapping
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found") from exc


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str) -> None:
    try:
        task_service.delete_task(UUID(task_id))
    except KeyError as exc:  # pragma: no cover - demo error mapping
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Task not found") from exc


@app.get("/pomodoro", response_model=PomodoroResponse)
def get_pomodoro() -> PomodoroResponse:
    return pomodoro_service.get_state()


@app.post("/pomodoro/start", response_model=PomodoroResponse)
def start_pomodoro(payload: PomodoroStartRequest | None = None) -> PomodoroResponse:
    try:
        return pomodoro_service.start(payload)
    except ValueError as exc:  # pragma: no cover - demo error mapping
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/pomodoro/stop", response_model=PomodoroResponse)
def stop_pomodoro() -> PomodoroResponse:
    return pomodoro_service.stop()


@app.post("/pomodoro/settings", response_model=PomodoroResponse)
def update_pomodoro_settings(settings: PomodoroSettings) -> PomodoroResponse:
    return pomodoro_service.update_settings(settings)


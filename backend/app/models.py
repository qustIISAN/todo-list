"""Pydantic models describing API payloads for the desktop widget backend."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field


class TaskCreate(BaseModel):
    """Payload for creating a task."""

    title: str = Field(..., min_length=1, max_length=200)


class TaskUpdate(BaseModel):
    """Payload for updating the completion state of a task."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    completed: Optional[bool] = None


class Task(TaskCreate):
    """Representation of a task exposed by the API."""

    id: UUID = Field(default_factory=uuid4)
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PomodoroSettings(BaseModel):
    """User-configurable pomodoro durations."""

    work_minutes: int = Field(25, ge=1, le=120)
    short_break_minutes: int = Field(5, ge=1, le=60)
    long_break_minutes: int = Field(15, ge=1, le=60)


class PomodoroState(BaseModel):
    """Runtime state of the pomodoro timer."""

    is_running: bool = False
    current_phase: str = "work"
    settings: PomodoroSettings = Field(default_factory=PomodoroSettings)
    started_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    completed_cycles: int = 0

    @property
    def remaining(self) -> Optional[timedelta]:
        if not self.is_running or not self.ends_at:
            return None
        delta = self.ends_at - datetime.utcnow()
        return max(delta, timedelta(0))

    @computed_field(return_type=float | None)
    def remaining_seconds(self) -> float | None:
        remaining = self.remaining
        return remaining.total_seconds() if remaining else None


class PomodoroStartRequest(BaseModel):
    """Request body for starting a pomodoro cycle."""

    phase: Optional[str] = Field(None, description="work | short_break | long_break")


class PomodoroResponse(BaseModel):
    """Response payload summarising pomodoro state."""

    state: PomodoroState


class TasksResponse(BaseModel):
    """Response payload providing task listings."""

    tasks: list[Task]


class TaskResponse(BaseModel):
    """Response payload for a single task."""

    task: Task


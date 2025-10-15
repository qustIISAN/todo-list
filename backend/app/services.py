"""Domain services for the desktop widget backend."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict
from uuid import UUID

from .models import (
    PomodoroResponse,
    PomodoroSettings,
    PomodoroStartRequest,
    PomodoroState,
    Task,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    TasksResponse,
)


class TaskService:
    """In-memory task manager suitable for early prototyping."""

    def __init__(self) -> None:
        self._tasks: Dict[UUID, Task] = {}

    def list_tasks(self) -> TasksResponse:
        return TasksResponse(tasks=list(self._tasks.values()))

    def create_task(self, payload: TaskCreate) -> TaskResponse:
        task = Task(title=payload.title)
        self._tasks[task.id] = task
        return TaskResponse(task=task)

    def update_task(self, task_id: UUID, payload: TaskUpdate) -> TaskResponse:
        if task_id not in self._tasks:
            raise KeyError(task_id)
        task = self._tasks[task_id]
        update_data = payload.dict(exclude_unset=True)
        if "title" in update_data:
            task.title = update_data["title"]
        if "completed" in update_data and update_data["completed"] is not None:
            task.completed = bool(update_data["completed"])
        self._tasks[task_id] = task
        return TaskResponse(task=task)

    def delete_task(self, task_id: UUID) -> None:
        if task_id not in self._tasks:
            raise KeyError(task_id)
        del self._tasks[task_id]


class PomodoroService:
    """Simple in-memory state container for a pomodoro timer."""

    PHASE_DURATIONS = {
        "work": lambda settings: timedelta(minutes=settings.work_minutes),
        "short_break": lambda settings: timedelta(minutes=settings.short_break_minutes),
        "long_break": lambda settings: timedelta(minutes=settings.long_break_minutes),
    }

    def __init__(self) -> None:
        self._state = PomodoroState()

    def get_state(self) -> PomodoroResponse:
        return PomodoroResponse(state=self._state)

    def start(self, payload: PomodoroStartRequest | None = None) -> PomodoroResponse:
        phase = payload.phase if payload and payload.phase else self._state.current_phase
        if phase not in self.PHASE_DURATIONS:
            raise ValueError(f"Unknown phase '{phase}'")

        duration = self.PHASE_DURATIONS[phase](self._state.settings)
        now = datetime.utcnow()
        self._state.is_running = True
        self._state.current_phase = phase
        self._state.started_at = now
        self._state.ends_at = now + duration
        if phase == "work":
            self._state.completed_cycles += 1
        return PomodoroResponse(state=self._state)

    def stop(self) -> PomodoroResponse:
        self._state.is_running = False
        self._state.started_at = None
        self._state.ends_at = None
        return PomodoroResponse(state=self._state)

    def update_settings(self, settings: PomodoroSettings) -> PomodoroResponse:
        self._state.settings = settings
        if self._state.is_running and self._state.started_at:
            phase = self._state.current_phase
            if phase in self.PHASE_DURATIONS:
                duration = self.PHASE_DURATIONS[phase](settings)
                self._state.ends_at = self._state.started_at + duration
        return PomodoroResponse(state=self._state)


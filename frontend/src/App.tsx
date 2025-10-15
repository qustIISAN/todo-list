import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";

type Task = {
  id: string;
  title: string;
  completed: boolean;
};

type PomodoroSettings = {
  work_minutes: number;
  short_break_minutes: number;
  long_break_minutes: number;
};

type PomodoroState = {
  state: {
    is_running: boolean;
    current_phase: string;
    started_at: string | null;
    ends_at: string | null;
    completed_cycles: number;
    remaining_seconds: number | null;
    settings: PomodoroSettings;
  };
};

const API_BASE_URL = (() => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL.replace(/\/$/, "");
  }
  if (typeof window !== "undefined" && window.location.port !== "5173") {
    return window.location.origin.replace(/\/$/, "");
  }
  return "http://localhost:8000";
})();

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return (await response.json()) as T;
}

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState("");
  const [pomodoro, setPomodoro] = useState<PomodoroState | null>(null);
  const [settingsDraft, setSettingsDraft] = useState<PomodoroSettings | null>(null);

  const loadTasks = useCallback(async () => {
    const data = await api<{ tasks: Task[] }>("/tasks");
    setTasks(data.tasks);
  }, []);

  const loadPomodoro = useCallback(async () => {
    const data = await api<PomodoroState>("/pomodoro");
    setPomodoro(data);
  }, []);

  useEffect(() => {
    loadTasks();
    loadPomodoro();
  }, [loadTasks, loadPomodoro]);

  useEffect(() => {
    if (pomodoro) {
      setSettingsDraft(pomodoro.state.settings);
    }
  }, [pomodoro]);

  const handleAddTask = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!newTask.trim()) {
      return;
    }
    const { task } = await api<{ task: Task }>("/tasks", {
      method: "POST",
      body: JSON.stringify({ title: newTask }),
    });
    setTasks((prev) => [...prev, task]);
    setNewTask("");
  };

  const toggleTask = async (task: Task) => {
    const { task: updated } = await api<{ task: Task }>(`/tasks/${task.id}`, {
      method: "PUT",
      body: JSON.stringify({ completed: !task.completed }),
    });
    setTasks((prev) => prev.map((item) => (item.id === updated.id ? updated : item)));
  };

  const deleteTask = async (task: Task) => {
    await fetch(`${API_BASE_URL}/tasks/${task.id}`, { method: "DELETE" });
    setTasks((prev) => prev.filter((item) => item.id !== task.id));
  };

  const startPomodoro = async (phase?: string) => {
    const response = await api<PomodoroState>("/pomodoro/start", {
      method: "POST",
      body: JSON.stringify(phase ? { phase } : {}),
    });
    setPomodoro(response);
  };

  const stopPomodoro = async () => {
    const response = await api<PomodoroState>("/pomodoro/stop", { method: "POST" });
    setPomodoro(response);
  };

  const handleSettingsChange = (field: keyof PomodoroSettings, value: number) => {
    setSettingsDraft((prev) =>
      prev
        ? {
            ...prev,
            [field]: value,
          }
        : prev,
    );
  };

  const applySettings = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!settingsDraft) {
      return;
    }
    const response = await api<PomodoroState>("/pomodoro/settings", {
      method: "POST",
      body: JSON.stringify(settingsDraft),
    });
    setPomodoro(response);
  };

  const remainingDisplay = useMemo(() => {
    if (!pomodoro?.state.remaining_seconds) {
      return "--:--";
    }
    const total = Math.max(0, Math.floor(pomodoro.state.remaining_seconds));
    const minutes = String(Math.floor(total / 60)).padStart(2, "0");
    const seconds = String(total % 60).padStart(2, "0");
    return `${minutes}:${seconds}`;
  }, [pomodoro]);

  return (
    <div className="widget">
      <header>
        <h1>Focus &amp; Tasks</h1>
        <p>Prototype desktop widget with Pomodoro timer and task list.</p>
      </header>

      <section className="section">
        <strong>Timer</strong>
        <div className="timer-display">{remainingDisplay}</div>
        <div className="button-row">
          <button className="primary" onClick={() => startPomodoro()}>Start</button>
          <button className="secondary" onClick={stopPomodoro}>Stop</button>
        </div>
        <div className="button-row">
          <button onClick={() => startPomodoro("short_break")}>Short break</button>
          <button onClick={() => startPomodoro("long_break")}>Long break</button>
        </div>
      </section>

      <section className="section">
        <strong>Settings</strong>
        <form className="settings-grid" onSubmit={applySettings}>
          {settingsDraft && (
            <>
              <label>
                Work (min)
                <input
                  type="number"
                  min={1}
                  max={120}
                  value={settingsDraft.work_minutes}
                  onChange={(event) => handleSettingsChange("work_minutes", Number(event.target.value))}
                />
              </label>
              <label>
                Short break (min)
                <input
                  type="number"
                  min={1}
                  max={60}
                  value={settingsDraft.short_break_minutes}
                  onChange={(event) =>
                    handleSettingsChange("short_break_minutes", Number(event.target.value))
                  }
                />
              </label>
              <label>
                Long break (min)
                <input
                  type="number"
                  min={1}
                  max={60}
                  value={settingsDraft.long_break_minutes}
                  onChange={(event) =>
                    handleSettingsChange("long_break_minutes", Number(event.target.value))
                  }
                />
              </label>
              <button className="primary" type="submit">
                Save settings
              </button>
            </>
          )}
        </form>
        <p className="helper-text">
          Adjust the timers to your preference, then click <em>Save settings</em>. Changes instantly
          update the current session.
        </p>
      </section>

      <section className="section">
        <strong>Tasks</strong>
        <form className="button-row" onSubmit={handleAddTask}>
          <input
            type="text"
            placeholder="Add a task"
            value={newTask}
            onChange={(event) => setNewTask(event.target.value)}
          />
          <button className="primary" type="submit">
            Add
          </button>
        </form>

        <ul className="task-list">
          {tasks.map((task) => (
            <li
              key={task.id}
              className={`task-item ${task.completed ? "completed" : ""}`.trim()}
            >
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => toggleTask(task)}
              />
              <span>{task.title}</span>
              <button className="secondary" onClick={() => deleteTask(task)}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}


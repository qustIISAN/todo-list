# Todo & Pomodoro Desktop Widget Demo

This repository contains a prototype for a desktop widget that combines a pomodoro timer and a checklist-oriented todo manager. The goal is to demonstrate a Python + web front-end architecture that can later be wrapped inside a desktop shell such as Tauri or Electron.

## Project structure

```
.
├── backend/              # FastAPI service exposing timer & todo APIs
│   ├── app/
│   │   ├── main.py       # FastAPI application wiring routes and services
│   │   ├── models.py     # Pydantic models shared across endpoints
│   │   └── services.py   # In-memory services for tasks and pomodoro logic
│   └── requirements.txt  # Python dependencies for the backend
├── frontend/             # Vite + React single page application
│   ├── index.html        # Entry point loaded by the dev server
│   ├── package.json      # Node dependencies and scripts
│   ├── src/              # React components and styling
│   └── vite.config.ts    # Vite configuration with backend proxy rules
└── README.md
```

## Getting started

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000 with the interactive documentation at http://localhost:8000/docs.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite development server will start on http://localhost:5173 and proxy `/api` requests to the FastAPI server.

## Next steps

* Wrap the FastAPI backend and React front-end using a desktop shell (e.g. Tauri, Electron, or neutral-ino) to deliver a native-like widget experience.
* Replace the in-memory stores with persistent storage (SQLite or other) and schedule background jobs for pomodoro notifications.
* Add automated tests and CI pipelines once the architecture stabilises.


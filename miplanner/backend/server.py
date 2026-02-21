"""Main server module."""

import glob
import json
import os
from datetime import datetime

from backend.planner import compute_schedule
from backend.repository import load_project, save_state
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Project

app = FastAPI()

app.mount("/static", StaticFiles(directory="miplanner/frontend/static"), name="static")

templates = Jinja2Templates(directory="miplanner/frontend/templates")


PROJECT_FILE = glob.glob("./projects/*.yaml")


def calculate_metrics(project: Project) -> dict:
    """Calculate metrics."""
    total_activities = len(project.activities)
    if total_activities == 0:
        completion = 0
    else:
        completion = sum(a.progress for a in project.activities) / total_activities

    # Estimated duration: sum of all activity estimates
    estimated_duration = sum(a.estimate_days for a in project.activities)
    done_activities = sum([1 for a in project.activities if a.progress == 100], 0)
    completion_activities = int(done_activities / total_activities * 100)

    # Actual duration: difference between first start and last end
    start_dates = [datetime.fromisoformat(a.actual_start) for a in project.activities if a.actual_start]
    end_dates = [datetime.fromisoformat(a.actual_end) for a in project.activities if a.actual_end]

    if start_dates and end_dates:
        actual_duration = (max(end_dates) - min(start_dates)).days
        completion_duration = min(100, int(actual_duration / estimated_duration * 100))
    else:
        actual_duration = None
        completion_duration = 0

    return {
        "completion": completion,
        "estimated_duration": estimated_duration,
        "actual_duration": actual_duration,
        "completion_duration": completion_duration,
        "total_activities": total_activities,
        "done_activities": done_activities,
        "completion_activities": completion_activities,
    }


@app.get("/")
def index(request: Request) -> Response:
    """Get index page."""
    project_summaries = []
    for p in PROJECT_FILE:
        project = load_project(os.path.basename(p))
        metrics = calculate_metrics(project)
        project_summaries.append({"name": project.name, "id": os.path.basename(p), "metrics": metrics})

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "projects": project_summaries,
        },
    )


@app.get("/project/{project_id}")
def get_project(request: Request, project_id: str) -> Response:
    """Get project page."""
    project = load_project(project_id)
    schedule = compute_schedule(project)

    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project": project,
            "schedule": schedule,
            "data": json.dumps([a.model_dump() for a in project.activities]),
            "metrics": calculate_metrics(project),
        },
    )


@app.post("/update")
def update_activity(activity_id: str = Form(...), progress: float = Form(...)) -> Response:
    """Update project state page."""
    project = load_project(PROJECT_FILE)

    for a in project.activities:
        if a.id == activity_id:
            a.progress = progress

    save_state(PROJECT_FILE, project)

    return RedirectResponse("/project", status_code=303)

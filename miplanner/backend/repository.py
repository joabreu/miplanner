"""Project repository module."""

from pathlib import Path

import yaml
from models import Activity, ActivityState, Project, ProjectPlan

PROJECT_DIR = Path("projects")


def load_project(project_file: str) -> Project:
    """Load project."""
    plan_path = PROJECT_DIR / project_file
    state_path = PROJECT_DIR / "state" / project_file
    state_path = state_path.with_suffix(".state.yaml")

    plan = ProjectPlan.model_validate(yaml.safe_load(plan_path.read_text()))

    if state_path.exists():
        raw = yaml.safe_load(state_path.read_text()) or {}
        state = {k: ActivityState(**v) for k, v in raw.items()}
    else:
        state = {}

    activities = []

    for a in plan.activities:

        s = state.get(a.id, ActivityState())

        activities.append(Activity(**a.model_dump(), **s.model_dump()))

    return Project(name=plan.name, start_date=plan.start_date, activities=activities)


def save_state(project_file: str, project: Project) -> None:
    """Save project state."""
    state_path = PROJECT_DIR / "state" / project_file
    state_path = state_path.with_suffix(".state.yaml")

    data = {}

    for a in project.activities:
        data[a.id] = {
            "progress": a.progress,
            "actual_start": a.actual_start,
            "actual_end": a.actual_end,
        }

    state_path.write_text(yaml.safe_dump(data))

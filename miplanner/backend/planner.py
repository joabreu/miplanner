"""Project planner module."""

from datetime import date, timedelta

from models import Activity, Project


def compute_schedule(project: Project) -> dict:
    """Compute project schedule."""
    cur = project.start_date
    schedule = {}

    for a in project.activities:

        start = cur
        end = start + timedelta(days=a.estimate_days)

        schedule[a.id] = {"start": start, "end": end}

        cur = end

    return schedule


def activity_status(activity: Activity, planned: dict) -> str:
    """Get project activity status."""
    today = date.today()

    start = planned["start"]
    end = planned["end"]

    total = (end - start).days
    elapsed = (today - start).days

    if total <= 0:
        return "invalid"

    expected = min(max(elapsed / total, 0), 1)

    if activity.progress >= expected:
        return "on_track"

    return "behind"

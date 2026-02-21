"""Project metrics module."""

from models import Project


def completion(project: Project) -> float:
    """Compute project completion."""
    if not project.activities:
        return 0

    return sum(a.progress for a in project.activities) / len(project.activities)


def estimated_duration(project: Project) -> int:
    """Compute project estimated duration in days."""
    return sum(a.estimate_days for a in project.activities)


def actual_duration(project: Project) -> int:
    """Compute project actual duration in days."""
    total = 0

    for a in project.activities:
        if a.actual_start and a.actual_end:
            total += (a.actual_end - a.actual_start).days

    return total

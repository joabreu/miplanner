"""Models for miplanner."""

from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ActivityPlan(BaseModel):
    """Project activity."""

    id: str
    name: str
    estimate_days: int = Field(gt=0)
    requirement: Optional[str] = None


class ProjectPlan(BaseModel):
    """Project."""

    name: str
    start_date: date
    activities: List[ActivityPlan]


class ActivityState(BaseModel):
    """State of project activity."""

    progress: int = Field(default=0, ge=0, le=100)
    actual_start: Optional[date] = None
    actual_end: Optional[date] = None


class ProjectState(BaseModel):
    """State of project."""

    activities: Dict[str, ActivityState] = {}


class Activity(BaseModel):
    """Project activity."""

    id: str
    name: str
    estimate_days: int
    requirement: Optional[str]
    progress: int = 0
    actual_start: Optional[date] = None
    actual_end: Optional[date] = None


class Project(BaseModel):
    """Project."""

    name: str
    start_date: date
    activities: List[Activity]

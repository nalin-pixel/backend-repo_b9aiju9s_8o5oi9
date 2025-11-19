"""
Self-Mastery App Schemas

Each Pydantic model below maps to a MongoDB collection using the lowercase
class name as the collection name (e.g., Habit -> "habit").

These schemas are used for validation at the API boundary.
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# Core user profile and preferences
class Profile(BaseModel):
    user_id: str = Field(..., description="Stable user identifier")
    name: str
    age_group: Literal["teen", "young_adult", "adult", "senior"]
    goals: List[str] = []
    discipline_score: float = 0.0
    theme: str = Field("neon-blue", description="Preferred theme name or hex")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Preferences(BaseModel):
    user_id: str
    theme_color: str = "#00E5FF"
    glow_intensity: float = Field(0.6, ge=0, le=1)
    card_opacity: float = Field(0.2, ge=0, le=1)
    font_family: str = "Inter"
    minimal_mode: bool = False
    notifications: bool = True
    backup_enabled: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Habit & routine
class Habit(BaseModel):
    user_id: str
    name: str
    icon: str = "Star"
    glow_color: str = "#7C3AED"  # purple
    schedule: List[str] = Field(default_factory=list, description="List of weekdays or cron-like strings")
    streak: int = 0
    analytics: dict = Field(default_factory=dict)
    archived: bool = False

class Routine(BaseModel):
    user_id: str
    period: Literal["morning", "afternoon", "night"]
    title: str
    tasks: List[dict] = Field(default_factory=list, description="[{ title, durationMinutes }]")
    animated: bool = True

# Tasks & productivity
class Task(BaseModel):
    user_id: str
    title: str
    notes: Optional[str] = None
    due_date: Optional[str] = None
    status: Literal["todo", "in_progress", "done"] = "todo"
    pomodoro_minutes: Optional[int] = 25
    order: int = 0

# Journal & mood
class JournalEntry(BaseModel):
    user_id: str
    date: str
    template: Literal["gratitude", "reflection", "ideas", "free"] = "free"
    content: str
    locked: bool = False

class Mood(BaseModel):
    user_id: str
    date: str
    mood: Literal["ecstatic", "happy", "calm", "neutral", "stressed", "sad"]
    reason: Optional[str] = None

# Money hub
class MoneyRecord(BaseModel):
    user_id: str
    date: str
    type: Literal["income", "expense", "saving"]
    amount: float
    note: Optional[str] = None

class SavingsGoal(BaseModel):
    user_id: str
    name: str
    target: float
    progress: float = 0.0

# Fitness & glow-up
class FitnessMetric(BaseModel):
    user_id: str
    date: str
    weight: Optional[float] = None
    steps: Optional[int] = None
    hydration_liters: Optional[float] = None
    skincare: List[str] = []
    gym_routine: List[dict] = []
    checklist: List[dict] = []

# Explore / challenges
class Challenge(BaseModel):
    user_id: Optional[str] = None
    slug: str
    title: str
    days: int
    category: Literal["discipline", "glowup", "money"]
    description: str

# AI Coach
class CoachPlan(BaseModel):
    user_id: str
    date: str
    summary: str
    focus: List[str] = []
    actions: List[dict] = []

# Export schema descriptions (for viewers)
class SchemaDescription(BaseModel):
    name: str
    fields: dict


def export_schemas() -> list[SchemaDescription]:
    models = [Profile, Preferences, Habit, Routine, Task, JournalEntry, Mood, MoneyRecord, SavingsGoal, FitnessMetric, Challenge, CoachPlan]
    out = []
    for m in models:
        out.append(SchemaDescription(name=m.__name__.lower(), fields=m.model_json_schema()))
    return out

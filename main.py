import os
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import (
    Profile,
    Preferences,
    Habit,
    Routine,
    Task,
    JournalEntry,
    Mood,
    MoneyRecord,
    SavingsGoal,
    FitnessMetric,
    Challenge,
    CoachPlan,
    export_schemas,
)

app = FastAPI(title="Self-Mastery API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "name": "Self-Mastery API"}


@app.get("/schema")
def get_schema():
    return [s.model_dump() for s in export_schemas()]


# Helper to insert and return
async def _insert(collection: str, payload: BaseModel):
    try:
        _id = create_document(collection, payload)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Onboarding/Profile
@app.post("/profile")
async def create_profile(profile: Profile):
    return await _insert("profile", profile)


@app.post("/preferences")
async def create_preferences(prefs: Preferences):
    return await _insert("preferences", prefs)


# Habits
@app.post("/habit")
async def create_habit(habit: Habit):
    return await _insert("habit", habit)


@app.get("/habit")
async def list_habits(user_id: str):
    try:
        docs = get_documents("habit", {"user_id": user_id})
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Routines
@app.post("/routine")
async def create_routine(routine: Routine):
    return await _insert("routine", routine)


@app.get("/routine")
async def list_routines(user_id: str):
    try:
        docs = get_documents("routine", {"user_id": user_id})
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Tasks
@app.post("/task")
async def create_task(task: Task):
    return await _insert("task", task)


@app.get("/task")
async def list_tasks(user_id: str):
    try:
        docs = get_documents("task", {"user_id": user_id})
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Journal
@app.post("/journal")
async def create_journal(entry: JournalEntry):
    return await _insert("journalentry", entry)


@app.get("/journal")
async def list_journal(user_id: str):
    try:
        docs = get_documents("journalentry", {"user_id": user_id})
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mood
@app.post("/mood")
async def create_mood(mood: Mood):
    return await _insert("mood", mood)


@app.get("/mood")
async def list_moods(user_id: str):
    try:
        docs = get_documents("mood", {"user_id": user_id})
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Money
@app.post("/money")
async def create_money(record: MoneyRecord):
    return await _insert("moneyrecord", record)


@app.get("/money")
async def list_money(user_id: str):
    try:
        docs = get_documents("moneyrecord", {"user_id": user_id})
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/savings-goal")
async def create_goal(goal: SavingsGoal):
    return await _insert("savingsgoal", goal)


@app.get("/savings-goal")
async def list_goals(user_id: str):
    try:
        docs = get_documents("savingsgoal", {"user_id": user_id})
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Fitness
@app.post("/fitness")
async def create_fitness(metric: FitnessMetric):
    return await _insert("fitnessmetric", metric)


@app.get("/fitness")
async def list_fitness(user_id: str):
    try:
        docs = get_documents("fitnessmetric", {"user_id": user_id})
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Challenges
PRESET_CHALLENGES = [
    {"slug": "discipline-7", "title": "7 Day Discipline", "days": 7, "category": "discipline", "description": "Build unstoppable momentum in a week."},
    {"slug": "glowup-30", "title": "30 Day Glow Up", "days": 30, "category": "glowup", "description": "Daily actions for visible improvement."},
    {"slug": "money-21", "title": "Money Sprint 21", "days": 21, "category": "money", "description": "Cash flow, skills, and savings."},
]


@app.get("/challenges")
async def list_challenges():
    return PRESET_CHALLENGES


# AI Coach (simple rules-based demo, cloud-ready)
@app.post("/coach/plan")
async def generate_coach_plan(user_id: str, mood: Optional[str] = None):
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        habits = get_documents("habit", {"user_id": user_id})
        routines = get_documents("routine", {"user_id": user_id})
        tasks = get_documents("task", {"user_id": user_id})
        recent_moods = get_documents("mood", {"user_id": user_id})[-7:]

        focus = []
        if mood in ("stressed", "sad"):
            focus += ["short wins", "breathing", "walk"]
        if len(tasks) > 5:
            focus += ["prioritize top 3"]
        if len(habits) < 3:
            focus += ["add a keystone habit"]
        if not focus:
            focus = ["consistency", "deep work", "hydration"]

        actions = [
            {"title": "10-min warmup", "time": "05:15"},
            {"title": "Deep work block", "time": "06:00"},
            {"title": "Move + hydrate", "time": "08:00"},
        ]
        plan = CoachPlan(user_id=user_id, date=today, summary="Personalized plan generated.", focus=focus, actions=actions)
        return await _insert("coachplan", plan)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            response["connection_status"] = "Connected"
            response["collections"] = db.list_collection_names()
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

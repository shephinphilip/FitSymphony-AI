# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
from agents.orchestrator import Orchestrator

app = FastAPI(title="FitSymphony AI – REST API", version="1.2.0")
orc = Orchestrator()

# -------------------------------
# Request Models
# -------------------------------
class ProfileRequest(BaseModel):
    user_id: str
    profile: Dict[str, Any]


class PlanRequest(BaseModel):
    user_id: str
    days: Optional[int] = 7
    profile: Optional[Dict[str, Any]] = None


class FeedbackRequest(BaseModel):
    user_id: str
    feedback_text: str


class ProgressRequest(BaseModel):
    user_id: str
    weight_kg: Optional[float] = None
    workout_minutes: Optional[int] = None
    kcals_burned: Optional[int] = None
    notes: Optional[str] = None


class AskRequest(BaseModel):
    user_id: str
    question: str


# -------------------------------
# Routes
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "agent": "FitSymphony AI"}


@app.post("/create_profile")
def create_profile(req: ProfileRequest):
    try:
        return orc.handle_event("create_profile", req.user_id, {"profile": req.profile})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_plan")
def generate_plan(req: PlanRequest):
    try:
        return orc.handle_event("generate_plan", req.user_id, req.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/submit_feedback")
def submit_feedback(req: FeedbackRequest):
    try:
        return orc.handle_event("submit_feedback", req.user_id, {"feedback_text": req.feedback_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/log_progress")
def log_progress(req: ProgressRequest):
    try:
        return orc.handle_event("log_progress", req.user_id, req.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask_ai")
def ask_ai(req: AskRequest):
    """Conversational endpoint that uses AskAgent via Orchestrator"""
    try:
        return orc.handle_event("ask_ai", req.user_id, {"question": req.question})
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

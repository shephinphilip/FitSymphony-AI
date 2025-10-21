# agents/progress_agent.py
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from .base_agent import STATE, log_event

class ProgressLog(BaseModel):
    date: Optional[str] = None
    weight_kg: Optional[float] = None
    workout_minutes: Optional[int] = None
    kcals_burned: Optional[int] = None
    notes: Optional[str] = None


class ProgressAgent:
    def log(self, user_id: str, entry: ProgressLog) -> None:
        """
        Log a new progress entry for a user.
        """
        STATE.append(user_id, "progress", entry.model_dump())
        log_event(user_id, "ProgressAgent", "log_progress", payload=entry.model_dump())

    def summarize(self, user_id: str) -> Dict[str, Any]:
        """
        Summarize user progress metrics (weight, duration, kcal averages).
        Returns safe defaults if no entries exist.
        """
        entries: List[Dict[str, Any]] = STATE.get(user_id, "progress", []) or []

        if not entries:
            return {"count": 0, "message": "No progress yet"}

        weights = [e.get("weight_kg", 0) for e in entries if e.get("weight_kg") is not None]
        durations = [e.get("workout_minutes", 0) for e in entries if e.get("workout_minutes") is not None]
        kcals = [e.get("kcals_burned", 0) for e in entries if e.get("kcals_burned") is not None]

        summary = {
            "count": len(entries),
            "avg_weight": round(sum(weights) / len(weights), 2) if weights else None,
            "avg_workout_minutes": round(sum(durations) / len(durations), 1) if durations else None,
            "avg_kcals_burned": round(sum(kcals) / len(kcals), 1) if kcals else None,
        }

        log_event(user_id, "ProgressAgent", "summarize", payload=summary)
        return summary
    


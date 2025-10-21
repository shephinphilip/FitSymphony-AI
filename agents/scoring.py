# agents/scoring.py
from typing import Dict, Any, List
from .base_agent import STATE, log_event

def adherence_score(user_id: str) -> float:
    """
    Compute user adherence score based on last 7 workout logs.
    Combines workout frequency and intensity consistency into a 0–100 score.
    """
    entries: List[Dict[str, Any]] = STATE.get(user_id, "progress", []) or []

    if not entries:
        return 0.0

    # Consider only last 7 logs
    recent_entries = entries[-7:] if len(entries) > 7 else entries
    mins = [e.get("workout_minutes", 0) for e in recent_entries if isinstance(e.get("workout_minutes"), (int, float))]

    if not mins:
        return 0.0

    target_min = 30
    hit_ratio = sum(1 for m in mins if m >= target_min) / len(mins)
    freq = len(mins) / 7.0  # normalized frequency factor

    score = round(50 * hit_ratio + 50 * min(freq, 1.0), 1)  # weighted 0–100
    log_event(user_id, "Scoring", "adherence_score", payload={"score": score})
    return score


def auto_tune_sets(current_sets: int, score: float, fatigue_flag: bool) -> int:
    """
    Automatically adjusts workout sets based on adherence and fatigue status.
    """
    sets = current_sets

    if fatigue_flag:
        sets = max(1, current_sets - 1)
    else:
        if score >= 80:
            sets = min(current_sets + 1, 5)
        elif score <= 40:
            sets = max(1, current_sets - 1)

    return sets

# agents/workout_agent.py
from typing import Dict, Any, List
from .base_agent import log_event

BASE_PLANS = {
    "Fat Loss": ["Jump Rope", "Mountain Climbers", "Cycling (Low Impact)", "Core Planks"],
    "Muscle Gain": ["Squats", "Deadlifts", "Bench Press", "Rows", "Overhead Press"],
    "Endurance": ["Cycling", "Jogging", "Rowing", "Swimming", "Elliptical"],
    "General Fitness": ["Yoga", "Brisk Walk", "Bodyweight Circuit", "Stretching", "Core Stability"]
}

class WorkoutAgent:
    def generate(self, user_id: str, profile: Dict[str, Any], days: int = 7) -> List[Dict[str, Any]]:
        goal = profile.get("goal", "General Fitness")
        level = profile.get("level", "Beginner")
        constraints = [c.lower() for c in profile.get("constraints", [])]

        base = BASE_PLANS.get(goal, BASE_PLANS["General Fitness"]).copy()

        # safety
        if any("injury" in c or "knee" in c for c in constraints):
            base = [x for x in base if "Jump Rope" not in x and "Mountain Climbers" not in x]
            if "Cycling (Low Impact)" not in base:
                base.append("Cycling (Low Impact)")

        volume = {"Beginner": 2, "Intermediate": 3, "Advanced": 4}.get(level, 2)

        plan = []
        for d in range(days):
            plan.append({"day": d + 1, "exercises": base[:3], "sets": volume, "notes": ""})

        log_event(user_id, "WorkoutAgent", "generate_plan", payload={"goal": goal, "level": level, "days": days})
        return plan

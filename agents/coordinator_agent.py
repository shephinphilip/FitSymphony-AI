# agents/coordinator_agent.py
from typing import Dict, Any, List
from .base_agent import log_event

class CoordinatorAgent:
    def resolve(self, user_id: str, profile: Dict[str, Any], workout: List[Dict[str, Any]], meals: List[Dict[str, Any]]) -> Dict[str, Any]:
        constraints = [c.lower() for c in profile.get("constraints", [])]
        reason = "ok"

        if any("injury" in c or "knee" in c for c in constraints):
            for day in workout:
                day["exercises"] = [ex for ex in day["exercises"] if "Jump Rope" not in ex and "Mountain Climbers" not in ex]
                if "Cycling (Low Impact)" not in day["exercises"]:
                    day["exercises"].append("Cycling (Low Impact)")
            reason = "enforced low-impact due to injury/knee constraint"

        log_event(user_id, "CoordinatorAgent", "resolve_conflicts", reason)
        return {"workout": workout, "meals": meals, "reason": reason}

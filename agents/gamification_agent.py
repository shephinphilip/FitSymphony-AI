# agents/gamification_agent.py
from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base_agent import STATE, log_event

class GamificationAgent:
    def _issue(self, user_id: str, badge: str, reason: str) -> None:
        badges: List[Dict[str, Any]] = STATE.get(user_id, "badges", []) or []
        if any(b.get("name") == badge for b in badges):
            return
        badges.append({
            "name": badge,
            "earned_at": datetime.utcnow().isoformat(),
            "reason": reason
        })
        STATE.set(user_id, "badges", badges)
        log_event(user_id, "GamificationAgent", "badge_awarded", reason, {"badge": badge})

    def evaluate(self, user_id: str) -> Dict[str, Any]:
        # Safely retrieve lists from STATE
        logs: List[Dict[str, Any]] = STATE.get(user_id, "progress", []) or []
        wearable: List[Dict[str, Any]] = STATE.get(user_id, "wearables", []) or []

        # --- Consistency badge ---
        recent_logs = [
            l for l in logs
            if l.get("date") and self._is_recent(l["date"], days=7)
        ]
        if len(recent_logs) >= 4:
            self._issue(user_id, "Consistency Star", "4+ logs this week")

        # --- Calorie control badge ---
        kcals = [l.get("kcals_burned", 0) for l in logs if l.get("kcals_burned") is not None]
        if kcals:
            avg_burn = sum(kcals) / len(kcals)
            if avg_burn >= 300:
                self._issue(user_id, "Calorie Controller", "Avg burn ≥ 300 kcals")

        # --- Step master badge ---
        if len(wearable) >= 3:
            steps = [w.get("steps", 0) for w in wearable[-3:]]
            if steps and sum(steps) / len(steps) >= 8000:
                self._issue(user_id, "Step Master", "Avg steps ≥ 8k (last 3)")

        # Return badges safely
        badges: List[Dict[str, Any]] = STATE.get(user_id, "badges", []) or []
        return {"badges": badges}

    # Utility: safely check recency
    @staticmethod
    def _is_recent(date_str: str, days: int = 7) -> bool:
        try:
            entry_date = datetime.fromisoformat(date_str)
            return entry_date >= datetime.utcnow() - timedelta(days=days)
        except Exception:
            return False

# agents/rl_adapter.py
from typing import Dict, Any, List
from .base_agent import log_event

class RLAdapter:
    """Placeholder for future supervised/RL personalization.
       Currently: simple rule using HR & sleep → delta to sets."""
    def suggest(self, user_id: str, profile: Dict[str, Any], plan: List[Dict[str, Any]], signal: Dict[str, Any]) -> Dict[str, Any]:
        hr = signal.get("hr_avg", 0)
        sleep = signal.get("sleep_hours", 7)
        adjust = 0
        if hr >= 95 and sleep < 6:
            adjust = -1
        log_event(user_id, "RLAdapter", "suggest", payload={"hr": hr, "sleep": sleep, "delta_sets": adjust})
        return {"delta_sets": adjust}

# agents/wearable_agent.py
from typing import Dict, Any
from .base_agent import STATE, log_event

# payload example:
# {"hr_rest":62,"hr_avg":96,"sleep_hours":5.8,"steps":9100,"vo2max":41.3,"date":"2025-10-14"}
class WearableAgent:
    def ingest(self, user_id: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        STATE.append(user_id, "wearables", metrics)
        log_event(user_id, "WearableAgent", "ingest_metrics", payload=metrics)
        return {"status": "ok"}

    def latest_signal(self, user_id: str) -> Dict[str, Any]:
        data = STATE.get(user_id, "wearables", [])
        return data[-1] if data else {}

# agents/base_agent.py
import time, uuid
from typing import Any, Dict, Optional, List

class MemoryStore:
    """
    Replace with MuleRun persistent state client in production.
    """
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def _ensure(self, user_id: str):
        if user_id not in self._store:
            self._store[user_id] = {
                "profile": None,
                "plans": {"workout": [], "nutrition": []},
                "progress": [],
                "wearables": [],
                "logs": [],
                "badges": []
            }

    def get(self, user_id: str, key: str, default=None):
        self._ensure(user_id)
        return self._store[user_id].get(key, default)

    def set(self, user_id: str, key: str, value: Any):
        self._ensure(user_id)
        self._store[user_id][key] = value

    def append(self, user_id: str, key: str, value: Any):
        self._ensure(user_id)
        self._store[user_id].setdefault(key, [])
        self._store[user_id][key].append(value)

STATE = MemoryStore()

def log_event(user_id: str, agent: str, action: str, reason: str = "", payload: Optional[dict] = None):
    entry = {
        "id": str(uuid.uuid4()),
        "ts": int(time.time()),
        "agent": agent,
        "action": action,
        "reason": reason,
        "payload": payload or {}
    }
    STATE.append(user_id, "logs", entry)

# agents/profile_agent.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .base_agent import STATE, log_event

class UserProfile(BaseModel):
    name: str
    age: int = Field(ge=12, le=100)
    goal: str = Field(description="Fat Loss | Muscle Gain | Endurance | General Fitness")
    level: str = Field(description="Beginner | Intermediate | Advanced")
    preferences: Optional[List[str]] = []
    constraints: Optional[List[str]] = []

class ProfileAgent:
    def upsert(self, user_id: str, profile: UserProfile) -> Dict[str, Any]:
        STATE.set(user_id, "profile", profile.dict())
        log_event(user_id, "ProfileAgent", "upsert_profile", payload=profile.dict())
        return profile.dict()

    def get(self, user_id: str) -> Optional[Dict[str, Any]]:
        return STATE.get(user_id, "profile")

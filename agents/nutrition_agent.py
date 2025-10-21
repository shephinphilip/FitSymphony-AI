# agents/nutrition_agent.py
import os
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv
from .base_agent import log_event

load_dotenv()

API_KEY = os.getenv("CALORIE_NINJAS_KEY","jtqSWZjl6fSoOrVgrqL8Eg==TGigqXTzIFXIScRC")
BASE_URL = "https://api.api-ninjas.com/v1/nutrition"


class NutritionAgent:
    def __init__(self):
        if not API_KEY:
            raise ValueError("CALORIE_NINJAS_KEY missing in .env")

    def _fetch_nutrition(self, query: str) -> List[Dict[str, Any]]:
        """Fetch nutrition info for a given food query."""
        try:
            headers = {"X-Api-Key": API_KEY}
            params = {"query": query}
            res = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
            if res.status_code == 200:
                return res.json()
            else:
                return [{"error": f"API returned {res.status_code}: {res.text}"}]
        except Exception as e:
            return [{"error": str(e)}]

    def generate(self, user_id: str, profile: Dict[str, Any], days: int = 7) -> List[Dict[str, Any]]:
        """Generate meal plan for the given profile."""
        meals = []
        goal = profile.get("goal", "").lower()

        # Basic mapping (can later use LLM-driven menu)
        if goal == "fat_loss":
            items = ["grilled chicken salad", "oatmeal with fruits", "boiled eggs"]
        elif goal == "muscle_gain":
            items = ["chicken breast rice", "protein shake", "scrambled eggs"]
        else:
            items = ["vegetable curry", "dal rice", "fruit smoothie"]

        for i, food in enumerate(items[:days]):
            nutrition_info = self._fetch_nutrition(food)
            meals.append({
                "day": i + 1,
                "item": food,
                "nutrition_info": nutrition_info
            })

        log_event(user_id, "NutritionAgent", "generate_meal_plan", payload={"meals": meals})
        return meals

    def adjust(self, user_id: str, adjustment_text: str):
        """Optional future: adjust meals via feedback text."""
        nutrition_info = self._fetch_nutrition(adjustment_text)
        log_event(user_id, "NutritionAgent", "adjust_meal", payload={"query": adjustment_text, "nutrition": nutrition_info})
        return nutrition_info

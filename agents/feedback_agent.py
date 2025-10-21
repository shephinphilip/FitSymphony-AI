from typing import Any, Dict, List, Union
from langchain.schema import BaseMessage
from .base_agent import log_event
from .langchain_core import feedback_chain
import json

class FeedbackAgent:
    def interpret(self, user_id: str, text: str) -> Union[Dict[str, Any], List[Any]]:
        try:
            result = feedback_chain.invoke({"feedback": text})

            if isinstance(result, BaseMessage):
                resp = result.content
            else:
                resp = result

            if isinstance(resp, (list, dict)):
                data = resp
            elif isinstance(resp, str):
                data = json.loads(resp)
            else:
                data = {}

        except Exception:
            data = {
                "workout_adjustment": "decrease intensity",
                "nutrition_adjustment": "",
                "reason": "parsed fallback"
            }

        # Ensure payload is always a dict
        if not isinstance(data, dict):
            payload = {"data": data}
        else:
            payload = data

        log_event(user_id, "FeedbackAgent", "llm_feedback_parse", payload=payload)
        return data

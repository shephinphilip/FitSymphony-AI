# agents/dynamic_rule_generator.py
import json
from typing import Dict, Any
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .base_agent import log_event

class DynamicRuleGenerator:
    def __init__(self):
        self.llm = ChatOllama(model="llama3", temperature=0.5)
        self.prompt = PromptTemplate.from_template("""
        You are a rule generator for a personalized fitness system.
        Based on the user's profile and feedback summary,
        create concise rule adjustments or safety guidelines.
        
        Profile:
        {profile}
        
        Feedback Summary:
        {feedback_summary}
        
        Output as plain text rules.
        """)
        self.chain = LLMChain(prompt=self.prompt, llm=self.llm)

    def generate(self, user_id: str, profile, feedback_summary: str) -> Dict[str, Any]:
        try:
            raw = self.chain.invoke({
                "profile": json.dumps(profile.model_dump(), indent=2),
                "feedback_summary": feedback_summary
            })
            text = raw.get("text", raw)
            log_event(user_id, "DynamicRuleGenerator", "rule_generation", payload={"rules": text})
            return {"rules": text}
        except Exception as e:
            log_event(user_id, "DynamicRuleGenerator", "error", payload={"error": str(e)})
            return {"rules": "default safety: limit overtraining; ensure hydration"}

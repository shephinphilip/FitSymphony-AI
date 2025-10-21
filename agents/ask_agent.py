# agents/ask_agent.py
import json
from typing import Dict, Any, List
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .base_agent import STATE, log_event


class AskAgent:
    """
    LLM-based question-answering agent that explains
    user's fitness plans, feedback, and progress history.
    """

    def __init__(self):
        self.llm = ChatOllama(model="llama3", temperature=0.4, num_ctx=4096)
        self.prompt = PromptTemplate.from_template("""
You are an explainable fitness assistant.
You have access to:
- user plans (workout + meals)
- agent logs (actions + reasons)
- rules that affected these plans

Answer the user's question in simple, supportive, and factual tone.
If the answer cannot be found, say "I don't have enough data to answer that."

USER QUESTION:
{question}

USER STATE DATA:
{context}

Your answer:
""")
        self.chain = LLMChain(prompt=self.prompt, llm=self.llm)

    def answer(self, user_id: str, question: str) -> Dict[str, Any]:
        # Collect contextual data
        plans = STATE.get(user_id, "plans", {}) or {}
        logs: List[Dict[str, Any]] = STATE.get(user_id, "logs", []) or []
        rules = STATE.get(user_id, "rules", {}) or {}

        context = {
            "plans": plans,
            "recent_logs": logs[-10:],
            "rules": rules,
        }

        try:
            # Replace chain.run with chain.invoke
            response = self.chain.invoke({
                "question": question,
                "context": json.dumps(context, indent=2)
            })
            # Extract text from the response object
            response_text = response.get('text', '')
        except Exception as e:
            response_text = f"Sorry, I couldn't process that: {e}"

        log_event(user_id, "AskAgent", "answer_question", question, {"response": response_text})
        return {"answer": response_text.strip()}

# agents/langchain_core.py
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

# --------------------------
# Initialize Ollama model
# --------------------------
# Supported local models: "llama3", "mistral", "phi3", etc.
llm = ChatOllama(
    model="llama3",
    temperature=0.5,
    num_ctx=4096,       # context length
    num_predict=512     # max tokens
)

# --------------------------
# FEEDBACK INTERPRETATION CHAIN
# --------------------------
feedback_prompt = PromptTemplate.from_template("""
You are a fitness AI assistant.
Given the user's feedback on their workout or diet, extract:
- workout_adjustment: describe changes like "increase sets" or "reduce intensity"
- nutrition_adjustment: describe food preference or swap
- reason: short justification
Respond ONLY in valid JSON.

User feedback: "{feedback}"
""")

# LCEL: pipe prompt → llm
feedback_chain = feedback_prompt | llm


# --------------------------
# RULE GENERATION CHAIN
# --------------------------
rule_prompt = PromptTemplate.from_template("""
You are a health and safety reasoning engine.
Given a user's profile and feedback summary, create safe adaptive fitness rules.
Each rule prevents injury or overtraining and improves adherence.
Return concise JSON like:
[{{"condition": "...", "action": "..."}}]

Profile: {profile}
Feedback Summary: {feedback_summary}
""")

# LCEL: pipe prompt → llm
rule_chain = rule_prompt | llm

# streamlit_app.py
import streamlit as st
import requests
import json

BASE_URL = "http://127.0.0.1:8000"  # Backend FastAPI endpoint

st.set_page_config(page_title="FitSymphony AI", layout="wide")

st.title("💪 FitSymphony AI – Your Personal Fitness Coach")

# -------------------------------
# Sidebar Navigation
# -------------------------------
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Create Profile", "📅 Generate Plan", "💬 Feedback", "📊 Log Progress", "🤖 Ask AI"]
)

st.sidebar.info("Use the sidebar to interact with your FitSymphony AI backend.")


# -------------------------------
# Helper to call backend
# -------------------------------
def call_api(endpoint, payload):
    try:
        res = requests.post(f"{BASE_URL}/{endpoint}", json=payload)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Error {res.status_code}: {res.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


# -------------------------------
# 1️⃣ Create Profile
# -------------------------------
if page == "🏠 Create Profile":
    st.header("👤 Create Your Fitness Profile")

    user_id = st.text_input("User ID", value="shephin")
    name = st.text_input("Name", "Shephin")
    age = st.number_input("Age", 18, 80, 24)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    goal = st.selectbox("Goal", ["fat_loss", "muscle_gain", "endurance", "general_fitness"])
    level = st.selectbox("Fitness Level", ["beginner", "intermediate", "advanced"])

    if st.button("Create Profile"):
        payload = {
            "user_id": user_id,
            "profile": {
                "name": name,
                "age": age,
                "gender": gender,
                "goal": goal,
                "level": level
            }
        }
        result = call_api("create_profile", payload)
        if result:
            st.success("Profile created successfully ✅")
            st.json(result)


# -------------------------------
# 2️⃣ Generate Plan
# -------------------------------
elif page == "📅 Generate Plan":
    st.header("📆 Generate Workout & Nutrition Plan")

    user_id = st.text_input("User ID", value="shephin")
    days = st.number_input("Days", 1, 7, 3)

    if st.button("Generate Plan"):
        payload = {"user_id": user_id, "days": days}
        result = call_api("generate_plan", payload)
        if result:
            st.subheader("🏋️ Workout Plan")
            st.json(result.get("workout_plan", []))
            st.subheader("🍱 Meal Plan (via CalorieNinjas API)")
            st.json(result.get("meal_plan", []))
            st.subheader("🧠 Rules & Insights")
            st.json(result.get("rules", {}))
            st.metric("Adherence Score", result.get("adherence_score", 0))


# -------------------------------
# 3️⃣ Submit Feedback
# -------------------------------
elif page == "💬 Feedback":
    st.header("💭 Share Your Feedback")

    user_id = st.text_input("User ID", value="shephin")
    feedback_text = st.text_area("Your feedback", "Increase intensity a bit today")

    if st.button("Submit Feedback"):
        payload = {"user_id": user_id, "feedback_text": feedback_text}
        result = call_api("submit_feedback", payload)
        if result:
            st.success("Feedback processed successfully ✅")
            st.subheader("Adjustment Summary")
            st.json(result.get("adjustment", {}))
            st.subheader("Updated Workout Plan")
            st.json(result.get("workout_plan", []))
            st.subheader("Updated Meal Plan")
            st.json(result.get("meal_plan", []))


# -------------------------------
# 4️⃣ Log Progress
# -------------------------------
elif page == "📊 Log Progress":
    st.header("📈 Log Daily Progress")

    user_id = st.text_input("User ID", value="shephin")
    weight = st.number_input("Weight (kg)", 30.0, 200.0, 75.0)
    minutes = st.number_input("Workout Minutes", 0, 300, 60)
    kcals = st.number_input("Calories Burned", 0, 1500, 350)
    notes = st.text_area("Notes", "Good energy levels today")

    if st.button("Log Progress"):
        payload = {
            "user_id": user_id,
            "weight_kg": weight,
            "workout_minutes": minutes,
            "kcals_burned": kcals,
            "notes": notes,
        }
        result = call_api("log_progress", payload)
        if result:
            st.success("Progress logged successfully ✅")
            st.json(result)


# -------------------------------
# 5️⃣ Ask AI
# -------------------------------
elif page == "🤖 Ask AI":
    st.header("🤖 Chat with FitSymphony AI")

    user_id = st.text_input("User ID", value="shephin")
    question = st.text_area("Ask your question", "What should I eat before my next workout?")

    if st.button("Ask"):
        payload = {"user_id": user_id, "question": question}
        result = call_api("ask_ai", payload)
        if result:
            st.subheader("💡 AI Response")
            st.write(result.get("answer", "No response"))

# agents/orchestrator.py
from typing import Dict, Any, List
from .base_agent import STATE, log_event
from .profile_agent import ProfileAgent, UserProfile
from .workout_agent import WorkoutAgent
from .nutrition_agent import NutritionAgent
from .feedback_agent import FeedbackAgent
from .coordinator_agent import CoordinatorAgent
from .dynamic_rule_generator import DynamicRuleGenerator
from .progress_agent import ProgressAgent, ProgressLog
from .wearable_agent import WearableAgent
from .gamification_agent import GamificationAgent
from .scoring import adherence_score, auto_tune_sets
from .rl_adapter import RLAdapter
from .ask_agent import AskAgent


class Orchestrator:
    def __init__(self):
        self.profile = ProfileAgent()
        self.workout = WorkoutAgent()
        self.nutrition = NutritionAgent()
        self.feedback = FeedbackAgent()
        self.coordinator = CoordinatorAgent()
        self.rules = DynamicRuleGenerator()
        self.progress = ProgressAgent()
        self.wearable = WearableAgent()
        self.gamify = GamificationAgent()
        self.rl = RLAdapter()
        self.ask = AskAgent()  # Using FeedbackAgent for Q&A functionality

    def handle_event(self, event: str, user_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        e = event.strip().lower()

        # -------------------------------
        # CREATE PROFILE
        # -------------------------------
        if e == "create_profile":
            prof = payload.get("profile", payload)
            profile = UserProfile(**prof)
            stored = self.profile.upsert(user_id, profile)
            log_event(user_id, "Orchestrator", "profile_created", payload=prof)
            return {"status": "ok", "profile": stored}

        # -------------------------------
        # GENERATE PLAN
        # -------------------------------
        if e == "generate_plan":
            days = int(payload.get("days", 7))
            profile_data = payload.get("profile")

            # Ensure profile exists
            if profile_data:
                stored = self.profile.upsert(user_id, UserProfile(**profile_data))
                profile = stored
            else:
                profile = self.profile.get(user_id)
                if not profile:
                    raise ValueError("No profile found. Call create_profile first.")

            # Generate workout and nutrition plans
            workout = self.workout.generate(user_id, profile, days)
            meals = self.nutrition.generate(user_id, profile, days)  # ← API call happens here

            # Feedback summary
            logs: List[Dict[str, Any]] = STATE.get(user_id, "logs", []) or []
            feedback_summary = " ".join(
                [l.get("payload", {}).get("reason", "") for l in logs if l.get("agent") == "FeedbackAgent"]
            )

            # Conflict resolution and rule generation
            resolved = self.coordinator.resolve(user_id, profile, workout, meals)
            llm_rules = self.rules.generate(user_id, profile, feedback_summary)

            # Wearable, adherence, and RL-based adjustments
            signal = self.wearable.latest_signal(user_id) or {}
            score = adherence_score(user_id)
            rl_suggestion = self.rl.suggest(user_id, profile, workout, signal) or {}
            delta = rl_suggestion.get("delta_sets", 0)
            fatigue_flag = (signal.get("hr_avg", 0) >= 100) or (signal.get("sleep_hours", 7) < 6)

            # Tune workouts dynamically
            for d in workout:
                tuned = auto_tune_sets(d.get("sets", 2), score, fatigue_flag)
                tuned += delta
                d["sets"] = max(1, min(5, tuned))

            # Save plan in memory
            STATE.set(user_id, "plans", {"workout": workout, "nutrition": meals})
            log_event(user_id, "Orchestrator", "store_plans", payload={"rules": llm_rules})

            return {
                "status": "ok",
                "workout_plan": workout,
                "meal_plan": meals,  # ✅ includes real nutrition data
                "rules": llm_rules,
                "adherence_score": score
            }

        # -------------------------------
        # 3. SUBMIT FEEDBACK
        # -------------------------------
        if e == "submit_feedback":
            fb_text = payload.get("feedback_text", "")
            if not fb_text:
                raise ValueError("feedback_text required")

            adj = self.feedback.interpret(user_id, fb_text) or {}
            plans = STATE.get(user_id, "plans", {"workout": [], "nutrition": []}) or {}
            workout = plans.get("workout", []) or []
            nutrition = plans.get("nutrition", []) or []

            # Ensure adj is a dictionary
            adj = adj if isinstance(adj, dict) else {}

            # Adjust intensity
            delta = adj.get("workout", {}).get("delta_sets", 0)
            if delta and workout:
                for d in workout:
                    d["sets"] = max(1, d.get("sets", 2) + delta)

            # Nutrition tweak
            nutrition_adj = adj.get("nutrition", {})
            if nutrition and isinstance(nutrition_adj, dict) and nutrition_adj.get("swap"):
                for d in nutrition:
                    d.setdefault("notes", "")
                    d["notes"] += " " + str(nutrition_adj.get("swap", ""))

            STATE.set(user_id, "plans", {"workout": workout, "nutrition": nutrition})
            log_event(user_id, "Orchestrator", "apply_feedback", payload=adj)
            return {"status": "ok", "adjustment": adj, "workout_plan": workout, "meal_plan": nutrition}

        # -------------------------------
        # 4. LOG PROGRESS
        # -------------------------------
        if e == "log_progress":
            entry = ProgressLog(**payload)
            self.progress.log(user_id, entry)
            log_event(user_id, "Orchestrator", "progress_logged", payload=entry.dict())
            return {"status": "ok", "message": "progress logged"}

        # -------------------------------
        # 5. GET PROGRESS
        # -------------------------------
        if e == "get_progress":
            summary = self.progress.summarize(user_id)
            logs: List[Dict[str, Any]] = STATE.get(user_id, "logs", []) or []
            return {"status": "ok", "summary": summary, "logs": logs[-50:]}

        # -------------------------------
        # 6. INGEST WEARABLE DATA
        # -------------------------------
        if e == "ingest_wearable":
            if not isinstance(payload, dict) or not payload:
                raise ValueError("wearable metrics required")
            result = self.wearable.ingest(user_id, payload)
            log_event(user_id, "Orchestrator", "wearable_ingested", payload=payload)
            return result

        # -------------------------------
        # 7. GAMIFICATION / BADGES
        # -------------------------------
        if e == "get_badges":
            badges = self.gamify.evaluate(user_id)
            log_event(user_id, "Orchestrator", "get_badges", payload=badges)
            return {"status": "ok", **badges}

        # -------------------------------
        # 8. METRICS / STATS
        # -------------------------------
        if e == "get_metrics":
            score = adherence_score(user_id)
            logs: List[Dict[str, Any]] = STATE.get(user_id, "logs", []) or []
            revisions = len([
                l for l in logs
                if l.get("action") in ("apply_feedback", "resolve_conflicts", "store_plans")
            ])
            metrics = {"adherence_score": score, "plan_revisions": revisions}
            log_event(user_id, "Orchestrator", "metrics", payload=metrics)
            return {"status": "ok", **metrics}
        

        # -------------------------------
        # ASK AI (Conversational Q&A)
        # -------------------------------
        if e == "ask_ai":
            question = payload.get("question", "")
            if not question.strip():
                raise ValueError("question text is required")
            response = self.ask.answer(user_id, question)
            return {"status": "ok", **response}



        # -------------------------------
        # INVALID EVENT
        # -------------------------------
        raise ValueError(
            f"Unsupported event '{event}'. Supported: "
            "create_profile, generate_plan, submit_feedback, "
            "log_progress, get_progress, ingest_wearable, get_badges, get_metrics"
        )

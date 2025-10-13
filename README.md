# FitSymphony AI – Multi-Agent Fitness and Nutrition Coach

## Overview

FitSymphony AI is an intelligent multi-agent system designed to deliver personalized, adaptive, and explainable fitness and nutrition recommendations.  
Unlike conventional fitness applications that provide static plans, FitSymphony AI employs multiple specialized agents that collaborate to continuously refine workout and nutrition plans based on user feedback, progress, and constraints.

The system dynamically resolves conflicts (such as dietary restrictions, injuries, or overtraining), tracks progress over time, and provides transparent, data-driven recommendations.  
It is implemented with a modular, explainable, and privacy-preserving architecture using LangChain, Streamlit, and local language models (Ollama).

---

## Core Objectives

- Generate custom workout and nutrition plans aligned with user goals.  
- Continuously adapt recommendations based on feedback and performance.  
- Resolve conflicts between user constraints such as injuries or dietary limits.  
- Track progress and analyze trends using structured fitness data.  
- Maintain transparency through explainable AI logs and rule-based reasoning.

---

## Detailed Use Case

### 1. User Onboarding

Users create a profile with details such as:
- Name, age, and gender  
- Fitness goal (fat loss, muscle gain, endurance, general fitness)  
- Fitness level (beginner, intermediate, advanced)  
- Preferences and restrictions (e.g., vegetarian, no running, asthma)

This data forms the foundation for generating the initial fitness and nutrition plans.

---

### 2. Plan Generation Phase

- The **Profile Agent** retrieves and validates user information.  
- The **Workout Agent** generates a structured workout plan for seven days.  
- The **Nutrition Agent** recommends meal plans and nutrition guidance.  
- The **Coordinator Agent** checks for conflicts and ensures safety.  
- The **Dynamic Rule Generator** creates fallback rules automatically for edge cases (e.g., replacing high-intensity workouts with low-impact alternatives).

All outputs are reviewed for coherence before being displayed to the user through the Streamlit interface.

---

### 3. Adaptive Feedback System

After completing workouts or meals, users can provide feedback such as “too intense,” “not tasty,” or “prefer vegetarian meals.”  
The **Feedback Agent** analyzes this input and communicates with other agents to adjust routines dynamically.  
Revised plans are generated instantly and stored with explanations in a shared log.

---

### 4. Progress Tracking and Analytics

The **Progress Agent** tracks body metrics, workout completion, calories burned, and performance patterns over time.  
Progress is visualized using charts and reports.  
Insights help users understand progress trends and identify areas for improvement.

---

### 5. Explainable Decision Logging

Every system action is recorded in `agent_logs.json` for transparency.  
Each log entry captures the agent name, timestamp, decision, and reason.

Example:
```json
{
  "timestamp": "2025-09-22T12:00:00",
  "agent": "WorkoutAgent",
  "action": "Increased workout intensity by 2 sets",
  "reason": "FeedbackAgent input: 'Workout was too easy'",
  "user_id": "Sunny"
}
````

These logs make AI reasoning auditable and verifiable.

---

## Architecture Overview

### Key Components

1. **Streamlit UI**

   * Provides a clean and interactive web interface.
   * Displays plans, progress charts, and insights.

2. **Local LLM (Ollama)**

   * Enables offline reasoning and natural language personalization.

3. **LangChain Orchestrator**

   * Handles data routing and communication between agents.

4. **Coordinator Agent**

   * Detects and resolves conflicts across all agent outputs.

5. **Dynamic Rule Generator**

   * Produces fallback logic for safe and adaptive plan generation.

---

## Agent Ecosystem

| Agent Name             | Description                                       | Data Source          |
| ---------------------- | ------------------------------------------------- | -------------------- |
| Profile Agent          | Manages user profiles and immutable constraints   | `user_profiles.json` |
| Workout Agent          | Generates and adapts workout plans                | `workouts.csv`       |
| Nutrition Agent        | Suggests meals with nutrition info                | Nutrition API        |
| Progress Agent         | Tracks metrics, trends, and performance           | `progress_data.csv`  |
| Feedback Agent         | Processes user input and improves personalization | `feedback_data.json` |
| Coordinator Agent      | Resolves conflicts and ensures safety             | Shared data layer    |
| Dynamic Rule Generator | Creates fallback rules dynamically                | All data sources     |
| Explainability Logger  | Records structured AI decisions                   | `agent_logs.json`    |

---

## System Workflow

1. User creates or updates a profile.
2. The system generates initial plans via the Profile, Workout, and Nutrition Agents.
3. The Coordinator Agent checks for conflicts.
4. The user follows the plan and provides feedback.
5. The Feedback Agent processes the response and triggers adjustments.
6. The Progress Agent logs metrics and visualizes improvements.
7. All decisions and actions are recorded for transparency.

---

## Technology Stack

* **Programming Language:** Python 3.10+
* **Frontend:** Streamlit
* **Orchestration:** LangChain
* **Local Model Runtime:** Ollama
* **External API:** Nutritionix API
* **Data Storage:** JSON, CSV
* **Version Control:** Git

---

## Installation and Setup

### Prerequisites

* Python 3.8 or higher
* Git installed
* Ollama for local LLM processing

### Steps

```bash
git clone https://github.com/Sridhar016/Fitness-tool-ai-multi-agent.git
cd ai-fitness-coach
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Configuration

Create a `.env` file:

```
NUTRITIONIX_APP_ID=your_app_id
NUTRITIONIX_API_KEY=your_api_key
```

---

## Example Workflow

**Example User:**
Name: Ben
Age: 21
Goal: Fat Loss
Level: Beginner
Preference: Vegetarian, mild asthma

1. The system generates a low-intensity workout plan.
2. Nutrition Agent builds vegetarian meal recommendations.
3. After feedback (“too intense”), Coordinator Agent triggers a new rule set that reduces cardio intensity.
4. Progress Agent records improvements in endurance and weight reduction.

---

## Key Advantages

* Multi-agent collaboration with scoped memory.
* Dynamic rule generation for personalized safety and flexibility.
* Adaptive feedback integration.
* Transparent explainability logs.
* Works offline using local language models.

---

## Future Enhancements

* Integration with wearable devices for real-time tracking.
* Voice-based interaction for accessibility.
* Predictive analytics for early fatigue or injury prevention.
* Cloud synchronization for multi-device access.
* Gamified progress dashboards for motivation.

---

## Conclusion

FitSymphony AI represents a new generation of intelligent, adaptive, and explainable fitness solutions.
By combining modular agent architecture, conflict resolution, adaptive learning, and transparent decision-making, it provides a personalized fitness journey that evolves alongside the user’s real-world performance.

---

## Author

**Shephin Philip**
Generative AI Engineer
Email: [shephinphilip.ai@gmail.com](mailto:shephinphilip786@gmail.com)
LinkedIn: [https://www.linkedin.com/in/shephinphilip](https://www.linkedin.com/in/shephin-philip-54b371205/)
GitHub: [https://github.com/ShephinPhilip](https://github.com/ShephinPhilip)

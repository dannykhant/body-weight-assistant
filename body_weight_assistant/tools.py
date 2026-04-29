"""Function tools for body weight assistant."""

import logging

from google.adk.tools.tool_context import ToolContext
from .models import UserInfoForm
import json
import time

def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict[str, str]:
    """Save the user's initial prompt to the state."""
    time.sleep(2)
    tool_context.state["prompt"] = prompt
    logging.info(f"[State updated] Added to prompt: {prompt}")
    return {"status": "success"}

def check_process_status(tool_context: ToolContext) -> dict[str, str]:
    """Checks the current status of the body weight assistance workflow."""
    state = tool_context.state
    
    # Check if already completed
    if "CoachAgent_output" in state:
        return {
            "action": "completed",
            "message": "Your weight management plan is already complete and has been delivered."
        }

    # Check if waiting for approval (after safeguard)
    if "SafeGuardAgent_output" in state:
        return {
            "action": "pending_approval",
            "message": "Your assessment results and safety checks are ready. Waiting for approval to generate the final guide.",
            "next_step_to_execute": "coach_agent"
        }

    # Check resume points
    if "prompt" in state:
        if "PlannerAgent_output" in state:
            return {
                "action": "resume",
                "next_step_to_execute": "safe_guard_agent"
            }
        if "BioCalculatorAgent_output" in state:
            return {
                "action": "resume",
                "next_step_to_execute": "planner_agent"
            }
        if "UserInfoAgent_output" in state:
            return {
                "action": "resume",
                "next_step_to_execute": "bio_calculator_agent"
            }
        return {
            "action": "resume",
            "next_step_to_execute": "userinfo_agent"
        }
        
    return {
        "action": "proceed_to_analysis",
        "message": "No existing process found. Starting a new weight management assessment."
    }

def save_user_intent(tool_context: ToolContext, intent: str) -> dict[str, str]:
    """Silently categorizes the user intent into the shared state."""
    time.sleep(2)
    tool_context.state["user_intent"] = intent
    logging.info(f"[State updated] Saved user_intent: {intent}")
    return {"status": "success"}

def calculate_all_biometrics(tool_context: ToolContext, weight_kg: float, height_cm: float, age_years: int, gender: str, activity_level: str) -> dict[str, any]:
    """Deterministically calculates BMI, BMR, and TDEE in one step."""
    time.sleep(2)
    # BMI
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 2)
    
    # BMR
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161
    bmr = round(bmr, 2)
    
    # TDEE
    multipliers = {
        'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very active': 1.9
    }
    tdee = round(bmr * multipliers.get(activity_level.lower(), 1.2), 2)
    
    results = {
        "bmi": bmi,
        "bmr": bmr,
        "tdee": tdee
    }
    
    tool_context.state["BioCalculatorAgent_output"] = json.dumps(results)
    logging.info(f"[State updated] Bio-metrics: {results}")
    return results

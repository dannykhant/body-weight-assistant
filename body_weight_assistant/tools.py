"""Function tools for body weight assistant."""

import logging

from google.adk.tools.tool_context import ToolContext
from .models import UserInfoForm

def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict[str, str]:
    """Save the user's initial prompt to the state."""
    tool_context.state["prompt"] = prompt
    logging.info(f"[State updated] Added to prompt: {prompt}")
    return {"status": "success"}

def check_process_status(tool_context: ToolContext) -> dict[str, str]:
    """Checks the current status of the body weight assistance workflow."""
    state = tool_context.state
    
    # Check if a process already exists
    if "user_info" in state and "research_findings" in state:
        # Check if already completed
        if "formatted_plan" in state:
            return {
                "action": "completed",
                "message": "Your weight management plan is already complete and has been delivered."
            }
        # Check if pending approval/finalization
        return {
            "action": "pending_approval",
            "message": "Your assessment results are ready. Waiting for approval to generate the final guide.",
            "next_step_to_execute": "response_formatter_agent"
        }
    
    # Check if we can resume from a specific point
    if "prompt" in state:
        if "user_info" in state:
            if "search_results" in state:
                 return {
                    "action": "resume",
                    "next_step_to_execute": "research_agent"
                }
            return {
                "action": "resume",
                "next_step_to_execute": "google_search_agent"
            }
        return {
            "action": "resume",
            "next_step_to_execute": "input_form_agent"
        }
        
    return {
        "action": "proceed_to_analysis",
        "message": "No existing process found. Starting a new weight management assessment."
    }



def save_research_findings(tool_context: ToolContext, findings: str) -> dict[str, str]:
    """Save the synthesized research findings to the state silently."""
    tool_context.state["research_findings"] = findings
    logging.info("[State updated] Saved research_findings.")
    return {"status": "success"}

def save_user_intent(tool_context: ToolContext, intent: str) -> dict[str, str]:
    """Silently categorizes the user intent into the shared state."""
    tool_context.state["user_intent"] = intent
    logging.info(f"[State updated] Saved user_intent: {intent}")
    return {"status": "success"}

def collect_user_info(tool_context: ToolContext, weight: float, target_weight: float, height: float, age: int, gender: str, activity_level: str, dietary_preference: str) -> str:
    """Collects user information and saves it for the response formatter."""
    form = UserInfoForm(
        weight=weight,
        target_weight=target_weight,
        height=height,
        age=age,
        gender=gender,
        activity_level=activity_level,
        dietary_preference=dietary_preference
    )
    tool_context.state["user_info"] = str(form)
    return f"Successfully processed user info: {form}"

"""tools for userinfo_agent."""

from google.adk.tools.tool_context import ToolContext
from .models import UserInfoData
import time
import logging

def collect_user_info(tool_context: ToolContext, weight: float, target_weight: float, height: float, age: int, gender: str, activity_level: str, dietary_preference: str) -> str:
    """Collects user information and saves it in the context state."""
    time.sleep(2)
    form = UserInfoData(
        weight=weight,
        target_weight=target_weight,
        height=height,
        age=age,
        gender=gender,
        activity_level=activity_level,
        dietary_preference=dietary_preference
    )
    tool_context.state["UserInfoAgent_output"] = form.model_dump_json()
    logging.info(f"Successfully collected user info: {tool_context.state['UserInfoAgent_output']}")
    return f"DATA_COLLECTED: All user metrics have been saved to state."


def pounds_to_kgs(weight: float) -> float:
    """Converts pounds to kgs."""
    return weight * 0.453592


def feet_to_inches(feet: float) -> float:
    """Converts feet to inches."""
    return feet * 12


def inches_to_cms(inches: float) -> float:
    """Converts inches to cms."""
    return inches * 2.54
"""userinfo_agent definition."""

from google.adk.agents.llm_agent import Agent
from .prompt import USERINFO_AGENT_PROMPT
from .models import UserInfoData
from .tools import pounds_to_kgs, feet_to_inches, inches_to_cms, collect_user_info


tools = [
    pounds_to_kgs,
    feet_to_inches,
    inches_to_cms,
    collect_user_info
]

from google.adk.models.google_llm import Gemini
from google.genai import types
import os

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=2.0, attempts=5, exp_base=2.0)

userinfo_agent = Agent(
    model=Gemini(
        model_name='gemini-2.5-flash',
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        retry_options=RETRY_OPTIONS
    ),
    name='userinfo_agent',
    description='Assistant who is specialized in collecting user information.',
    instruction=USERINFO_AGENT_PROMPT,
    tools=tools,
    output_schema=UserInfoData
)

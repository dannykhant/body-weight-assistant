"""safeguard agent definition"""

from google.adk.agents.llm_agent import Agent
from .prompt import SAFE_GUARD_AGENT_PROMPT
from .models import SafetyValidation

from google.adk.models.google_llm import Gemini
from google.genai import types
import os

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=2.0, attempts=5, exp_base=2.0)

safe_guard_agent = Agent(
    model=Gemini(
        model_name='gemini-2.5-flash',
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        retry_options=RETRY_OPTIONS
    ),
    name='safe_guard_agent',
    description='An agent responsible for the safety and reasonableness of the fitness and diet plans provided to users.',
    instruction=SAFE_GUARD_AGENT_PROMPT,
    output_schema=SafetyValidation,
)

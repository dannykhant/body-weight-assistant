"""coach agent definition"""

from google.adk.agents.llm_agent import Agent
from .prompt import COACH_AGENT_PROMPT
from .models import CoachResponse

from google.adk.models.google_llm import Gemini
from google.genai import types
import os

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=2.0, attempts=5, exp_base=2.0)

coach_agent = Agent(
    model=Gemini(
        model_name='gemini-2.5-flash',
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        retry_options=RETRY_OPTIONS
    ),
    name='coach_agent',
    description='An expert coach agent that motivates and guides users through their fitness journey.',
    instruction=COACH_AGENT_PROMPT,
    output_schema=CoachResponse,
)

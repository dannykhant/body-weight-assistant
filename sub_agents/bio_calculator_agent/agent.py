"""bio calculator agent definition."""

from google.adk.agents.llm_agent import Agent
from .prompt import BIO_CALCULATOR_AGENT_PROMPT
from .models import BioMetricsData
from .tools import calculate_bmi, calculate_bmr, calculate_tdee

from google.adk.models.google_llm import Gemini
from google.genai import types
import os

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=2.0, attempts=5, exp_base=2.0)

bio_calculator_agent = Agent(
    model=Gemini(
        model_name='gemini-2.5-flash',
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        retry_options=RETRY_OPTIONS
    ),
    name='bio_calculator_agent',
    description="An assistant to calculate user's bio metrics",
    instruction=BIO_CALCULATOR_AGENT_PROMPT,
    tools=[calculate_bmi, calculate_bmr, calculate_tdee],
    output_schema=BioMetricsData,
)

"""planner agent definition."""

from google.adk.agents.llm_agent import Agent
from .prompt import PLANNER_AGENT_PROMPT
from .models import FitnessPlan
from google.adk.tools.google_search_agent_tool import GoogleSearchAgentTool, create_google_search_agent
from .tools import fitness_research_tool

# Wrap google_search in an AgentTool to allow mixing with functional tools
google_search_wrapped = GoogleSearchAgentTool(agent=create_google_search_agent(model='gemini-2.5-flash'))

from google.adk.models.google_llm import Gemini
from google.genai import types
import os

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=2.0, attempts=5, exp_base=2.0)

planner_agent = Agent(
    model=Gemini(
        model_name='gemini-2.5-flash',
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        retry_options=RETRY_OPTIONS
    ),
    name='planner_agent',
    description='An expert fitness planner agent that creates comprehensive diet and workout plans.',
    instruction=PLANNER_AGENT_PROMPT,
    tools=[fitness_research_tool, google_search_wrapped],
    output_schema=FitnessPlan,
)
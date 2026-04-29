"""
ADK Agent for body weight assistant.

Orchestrator based agent architecture with sub-agents.
"""


from google.adk.tools import AgentTool
from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types
import os

# Define retry options for Gemini models
RETRY_OPTIONS = types.HttpRetryOptions(
    initial_delay=2.0,
    attempts=5,
    exp_base=2.0
)

from .tools import add_prompt_to_state, check_process_status, save_user_intent, calculate_all_biometrics
from sub_agents.userinfo_agent.agent import userinfo_agent
from sub_agents.bio_calculator_agent.agent import bio_calculator_agent
from sub_agents.planner_agent.agent import planner_agent
from sub_agents.coach_agent.agent import coach_agent
from sub_agents.safe_guard_agent.agent import safe_guard_agent
from .prompt import ORCHESTRATOR_PROMPT

root_agent = Agent(
    model=Gemini(
        model_name='gemini-2.5-flash',
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        retry_options=RETRY_OPTIONS
    ),
    name='root_agent',
    description='The central orchestrator for the Body Weight Assistant.',
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        AgentTool(userinfo_agent),
        AgentTool(bio_calculator_agent),
        AgentTool(planner_agent),
        AgentTool(safe_guard_agent),
        AgentTool(coach_agent),
        add_prompt_to_state,
        check_process_status,
        save_user_intent,
        calculate_all_biometrics
    ]
)

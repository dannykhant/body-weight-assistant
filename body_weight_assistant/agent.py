"""
ADK Agent for body weight assistant.

Orchestrator based agent architecture with sub-agents.
"""


from google.adk.tools import AgentTool
from google.adk.agents.llm_agent import Agent

from .tools import add_prompt_to_state, check_process_status, save_user_intent, save_research_findings, collect_user_info
from .sub_agents import input_form_agent, google_search_agent, research_agent, response_formatter_agent, guardrail_agent
from .prompt import ORCHESTRATOR_PROMPT


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='The central orchestrator for the Body Weight Assistant.',
    instruction=ORCHESTRATOR_PROMPT,
    tools=[
        AgentTool(input_form_agent),
        AgentTool(google_search_agent),
        AgentTool(research_agent),
        AgentTool(response_formatter_agent),
        AgentTool(guardrail_agent),
        add_prompt_to_state,
        check_process_status,
        collect_user_info,
        save_user_intent,
        save_research_findings
    ]
)

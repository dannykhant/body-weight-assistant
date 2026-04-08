import pytest
from unittest.mock import MagicMock

from body_weight_assistant.sub_agents import input_form_agent, research_agent, response_formatter_agent, google_search_agent
from body_weight_assistant.agent import root_agent
from body_weight_assistant.models import UserInfoForm
from body_weight_assistant.tools import (
    add_prompt_to_state, 
    check_process_status, 
    save_user_intent, 
    save_research_findings, 
    collect_user_info
)
from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool
from google.adk.tools.google_search_tool import google_search

# Sub-Agent Tests
def test_input_form_agent_configuration():
    assert input_form_agent.name == "input_form_agent"
    assert input_form_agent.model == "gemini-2.5-flash"
    assert len(input_form_agent.tools) == 0  # Orchestrated sub-agents are pure executors

def test_google_search_agent_configuration():
    assert google_search_agent.name == "google_search_agent"
    assert google_search in google_search_agent.tools

def test_research_agent_configuration():
    assert research_agent.name == "research_agent"
    assert research_agent.model == "gemini-2.5-flash"
    assert len(research_agent.tools) == 0

def test_response_formatter_agent_configuration():
    assert response_formatter_agent.name == "response_formatter_agent"
    assert "synthesized background research" in response_formatter_agent.instruction.lower()

# Orchestrator Tests
def test_root_agent_configuration():
    assert isinstance(root_agent, Agent)
    assert root_agent.name == "root_agent"
    
    # Check for functional tools
    tool_funcs = [t for t in root_agent.tools if not isinstance(t, AgentTool)]
    assert add_prompt_to_state in tool_funcs
    assert check_process_status in tool_funcs
    assert collect_user_info in tool_funcs
    assert save_user_intent in tool_funcs
    assert save_research_findings in tool_funcs

    # Check for sub-agent tools
    agent_tool_names = [t.agent.name for t in root_agent.tools if isinstance(t, AgentTool)]
    assert "input_form_agent" in agent_tool_names
    assert "google_search_agent" in agent_tool_names
    assert "research_agent" in agent_tool_names
    assert "response_formatter_agent" in agent_tool_names

# Logic & Status Tests
def test_check_process_status_new():
    mock_context = MagicMock()
    mock_context.state = {}
    result = check_process_status(mock_context)
    assert result["action"] == "proceed_to_analysis"

def test_check_process_status_resume_input_form():
    mock_context = MagicMock()
    mock_context.state = {"prompt": "I want to lose 5kg"}
    result = check_process_status(mock_context)
    assert result["action"] == "resume"
    assert result["next_step_to_execute"] == "input_form_agent"

def test_check_process_status_pending_approval():
    mock_context = MagicMock()
    mock_context.state = {
        "user_info": "weight: 80, target: 75",
        "research_findings": "High protein diet suggested"
    }
    result = check_process_status(mock_context)
    assert result["action"] == "pending_approval"
    assert result["next_step_to_execute"] == "response_formatter_agent"

def test_add_prompt_to_state():
    mock_context = MagicMock()
    mock_context.state = {}
    add_prompt_to_state(mock_context, "Goal: muscle gain")
    assert mock_context.state["prompt"] == "Goal: muscle gain"

def test_collect_user_info_logic():
    mock_context = MagicMock()
    mock_context.state = {}
    collect_user_info(mock_context, 80.0, 75.0, 180.0, 30, "male", "active", "none")
    assert "user_info" in mock_context.state
    assert "weight=80.0" in mock_context.state["user_info"]

# Model Test
def test_user_info_schema():
    form = UserInfoForm(
        weight=80.5,
        target_weight=75.0,
        height=180.0,
        age=30,
        gender="male",
        activity_level="high",
        dietary_preference="vegan"
    )
    assert form.weight == 80.5
    assert form.age == 30

import pytest
from unittest.mock import MagicMock, patch

from body_weight_assistant.agent import root_agent
from body_weight_assistant.tools import (
    add_prompt_to_state, 
    check_process_status, 
    save_user_intent,
    calculate_all_biometrics
)
from sub_agents.userinfo_agent.agent import userinfo_agent
from sub_agents.planner_agent.agent import planner_agent
from sub_agents.safe_guard_agent.agent import safe_guard_agent

# Internal bio-calculation functions are now tested via calculate_all_biometrics
from sub_agents.userinfo_agent.tools import (
    pounds_to_kgs,
    feet_to_inches,
    inches_to_cms,
    collect_user_info
)
from sub_agents.planner_agent.tools import fitness_research_tool

from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool

# --- Agent Configuration Tests ---

def test_userinfo_agent_config():
    assert userinfo_agent.name == "userinfo_agent"
    assert userinfo_agent.model == "gemini-2.5-flash"
    assert collect_user_info in userinfo_agent.tools

# bio_calculator_agent has been replaced by a direct tool

def test_planner_agent_config():
    assert planner_agent.name == "planner_agent"
    assert fitness_research_tool in planner_agent.tools

def test_root_agent_config():
    assert isinstance(root_agent, Agent)
    assert root_agent.name == "root_agent"
    
    agent_tool_names = [t.agent.name for t in root_agent.tools if isinstance(t, AgentTool)]
    expected_agents = ["userinfo_agent", "planner_agent", "safe_guard_agent"]
    for agent_name in expected_agents:
        assert agent_name in agent_tool_names

    tool_funcs = [t for t in root_agent.tools if not isinstance(t, AgentTool)]
    assert add_prompt_to_state in tool_funcs
    assert check_process_status in tool_funcs
    assert save_user_intent in tool_funcs
    assert calculate_all_biometrics in tool_funcs

# --- Orchestrator Tool Tests ---

def test_check_process_status_initial():
    mock_context = MagicMock()
    mock_context.state = {}
    result = check_process_status(mock_context)
    assert result["action"] == "proceed_to_analysis"

def test_check_process_status_resume_userinfo():
    mock_context = MagicMock()
    mock_context.state = {"prompt": "Start diet"}
    result = check_process_status(mock_context)
    assert result["action"] == "resume"
    assert result["next_step_to_execute"] == "userinfo_agent"

def test_check_process_status_resume_biocalc():
    mock_context = MagicMock()
    mock_context.state = {"prompt": "Start", "UserInfoAgent_output": "data"}
    result = check_process_status(mock_context)
    assert result["next_step_to_execute"] == "bio_calculator_agent"

def test_check_process_status_pending_approval():
    mock_context = MagicMock()
    mock_context.state = {
        "prompt": "Start",
        "UserInfoAgent_output": "data",
        "BioCalculatorAgent_output": "data",
        "PlannerAgent_output": "data",
        "SafeGuardAgent_output": {"is_safe": True}
    }
    result = check_process_status(mock_context)
    assert result["action"] == "pending_approval"
    assert result["next_step_to_execute"] == "coach_agent"

# --- Bio Calculator Tool Tests ---

def test_calculate_all_biometrics():
    mock_context = MagicMock()
    mock_context.state = {}
    # 70kg, 175cm, 25yr male, active
    # BMI: 70 / (1.75^2) = 22.86
    # BMR: 10*70 + 6.25*175 - 5*25 + 5 = 1673.75
    # TDEE: 1673.75 * 1.725 = 2887.22
    result = calculate_all_biometrics(mock_context, 70, 175, 25, "male", "active")
    assert result["bmi"] == 22.86
    assert result["bmr"] == 1673.75
    assert result["tdee"] == 2887.22
    assert "BioCalculatorAgent_output" in mock_context.state

# --- User Info Tool Tests ---

def test_unit_conversions():
    assert pytest.approx(pounds_to_kgs(100), 0.01) == 45.36
    assert feet_to_inches(5) == 60
    assert inches_to_cms(10) == 25.4

def test_collect_user_info_state_update():
    mock_context = MagicMock()
    mock_context.state = {}
    collect_user_info(mock_context, 80, 75, 180, 30, "male", "active", "none")
    assert "UserInfoAgent_output" in mock_context.state
    assert '"weight":80.0' in mock_context.state["UserInfoAgent_output"]

# --- Planner Tool Tests ---

@patch("sub_agents.planner_agent.tools.hierarchical_fitness_search")
def test_fitness_research_tool_call(mock_search):
    mock_search.return_value = "Mocked results"
    result = fitness_research_tool("how to lose weight")
    mock_search.assert_called_once_with("how to lose weight")
    assert result == "Mocked results"

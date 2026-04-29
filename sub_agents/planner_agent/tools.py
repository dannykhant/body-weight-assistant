"""tools for planner agent"""
import sys
import os

# Ensure the root directory is in sys.path so we can import body_weight_assistant.utils
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from body_weight_assistant.utils.grounding import hierarchical_fitness_search
import time

def fitness_research_tool(query: str) -> str:
    """
    Research fitness, diet, and health data using a hierarchical approach.
    It first attempts to retrieve data from the internal Vertex AI Data Store.
    If results are insufficient, it falls back to Google Search.
    """
    time.sleep(3)
    return hierarchical_fitness_search(query)

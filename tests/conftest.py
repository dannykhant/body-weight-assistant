import sys
import os

# Ensure the 'body_weight_assistant' package is in the Python path
# This allows running tests from the root or tests/ directory without ModuleNotFoundError
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
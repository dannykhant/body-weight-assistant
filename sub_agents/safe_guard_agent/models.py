"""data models for safe guard agent"""
from pydantic import BaseModel, Field

class SafetyValidation(BaseModel):
    is_safe: bool = Field(description="True if the plan meets all safety guidelines, False otherwise.")
    reason: str = Field(description="Explanation for the safety decision.")
    suggested_modifications: str = Field(description="Specific suggestions to make the plan safer if is_safe is False.")
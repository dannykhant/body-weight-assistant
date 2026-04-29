"""data models for userinfo_agent."""

from pydantic import BaseModel, Field


class UserInfoData(BaseModel):
    weight: float = Field(description="User's current weight in kgs")
    target_weight: float = Field(description="User's target weight in kgs")
    height: float = Field(description="User's height in cms")
    age: int = Field(description="User's age")
    gender: str = Field(description="User's gender (e.g., 'male', 'female', 'other')")
    activity_level: str = Field(description="User's activity level (e.g., 'high', 'medium', 'low')")
    dietary_preference: str = Field(description="User's dietary preference (e.g., 'low-carb', 'gluten-free', 'vegan', 'none')")
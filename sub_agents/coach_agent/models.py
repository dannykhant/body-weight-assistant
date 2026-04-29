"""data models for coach agent"""
from pydantic import BaseModel, Field

class CoachResponse(BaseModel):
    message: str = Field(description="The final personalized coach message in Markdown format")
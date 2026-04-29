"""data models for bio calculator agent."""

from pydantic import BaseModel, Field

class BioMetricsData(BaseModel):
    bmi: float = Field(description="The calculated Body Mass Index (BMI)")
    bmr: float = Field(description="The calculated Basal Metabolic Rate (BMR)")
    tdee: float = Field(description="The calculated Total Daily Energy Expenditure (TDEE)")

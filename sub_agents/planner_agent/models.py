"""data models for planner agent."""
from pydantic import BaseModel, Field

class DietPlan(BaseModel):
    daily_calories: int = Field(description="Target daily calorie intake")
    macros: str = Field(description="Recommended macro-nutrient split (e.g., 40% Protein, 40% Carbs, 20% Fats)")
    meal_suggestions: list[str] = Field(description="List of suggested meals or foods tailored to dietary preference")

class WorkoutPlan(BaseModel):
    frequency_per_week: int = Field(description="Number of workout days per week")
    workout_type: str = Field(description="Type of workout (e.g., strength training, cardio, mixed)")
    routine_suggestions: list[str] = Field(description="List of suggested exercises or routines")

class FitnessPlan(BaseModel):
    goal_summary: str = Field(description="Summary of the user's fitness goal based on their metrics")
    diet: DietPlan = Field(description="The recommended diet plan")
    workout: WorkoutPlan = Field(description="The recommended workout plan")
    estimated_timeline_weeks: int = Field(description="Estimated number of weeks to achieve the target weight")
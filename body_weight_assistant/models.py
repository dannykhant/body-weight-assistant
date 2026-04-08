from pydantic import BaseModel, Field

class UserInfoForm(BaseModel):
    weight: float = Field(description="Your current weight")
    target_weight: float = Field(description="Your target weight")
    height: float = Field(description="Your height")
    age: int = Field(description="Your age")
    gender: str = Field(description="Your gender")
    activity_level: str = Field(description="Your activity level")
    dietary_preference: str = Field(description="Your dietary preference")
    
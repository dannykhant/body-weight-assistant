"""tools for bio calculator agent."""

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate Body Mass Index (BMI)."""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def calculate_bmr(weight_kg: float, height_cm: float, age_years: int, gender: str) -> float:
    """Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation."""
    if gender.lower() == 'male':
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years + 5
    else:
        # Female or other as fallback
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age_years - 161
    return round(bmr, 2)

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Calculate Total Daily Energy Expenditure (TDEE) based on activity level."""
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very active': 1.9
    }
    # Fallback to sedentary if activity level is unknown
    multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
    tdee = bmr * multiplier
    return round(tdee, 2)

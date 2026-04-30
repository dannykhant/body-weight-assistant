"""Agent tools for body weight assistant."""

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import google_search



response_formatter_agent = Agent(
    model='gemini-2.5-flash',
    name='response_formatter_agent',
    description='Assistant who is specialized in formatting the response for the user.',
    instruction='''
    You are an empathetic and motivating fitness coach.
    
    TASK: Take the synthesized background research findings and formulate a comprehensive, polite, and actionable final response.
    
    1. Customize the advice to the user's specific goals, age, and metrics.
    2. Use clean Markdown formatting, bullet points, and headers for readability.
    3. Ensure the tone is encouraging but professional.
    4. Always include a brief disclaimer that this is AI-generated advice and they should consult a medical professional before making extreme lifestyle changes.
    '''
)

guardrail_agent = Agent(
    model='gemini-2.5-flash',
    name='guardrail_agent',
    description='Assistant specialized in auditing fitness plans for safety.',
    instruction='''
    You are a health and safety auditor. 
    Your task is to review the synthesized fitness and diet plan provided to you.
    
    CHECK FOR:
    1. Extreme calorie deficits (e.g., suggesting < 1200 calories for adults).
    2. Promotion of dangerous supplements or "fad" diets.
    3. Excessive exercise routines that could lead to injury.
    
    Output ONLY "APPROVED" if the plan is safe, or "REJECTED: [Reason]" if it poses a health risk.
    '''
)

research_agent = Agent(
    model='gemini-2.5-flash',
    name='research_agent',
    description='Assistant who is specialized in synthesizing fitness and diet plans.',
    instruction='''
    You are a background fitness research synthesizer.
    Your job is to read the raw data from `SEARCH RESULTS` and logically construct a highly detailed, comprehensive dietary and workout plan.
    
    1. Align the plan with the user's exact metrics: weight, target_weight, height, age, gender, activity_level, and dietary_preferences.
    2. Focus on specific calorie goals, macro-nutrient splits, and workout frequency.
    3. If safety feedback is provided (from a "REJECTED" status), you MUST modify the plan to resolve the specific health risks mentioned while keeping the user's goals in mind.
    4. Output the synthesized plan in full detail first.
    5. END your response with a concise line: "Synthesis Complete: Finalized personalized plan for the user's [user_intent] goal."
    ''',
)

google_search_agent = Agent(
    model='gemini-2.5-flash',
    name='google_search_agent',
    description='Assistant who is specialized in executing online web searches.',
    instruction='''
    You are a background data retriever specializing in fitness and nutrition analytics.
    Use the identified user intent and metrics to execute targeted Google searches.
    
    GOAL: Find authoritative macro-nutrient breakdowns, meal suggestions, and weekly exercise routines tailored specifically to the user's age, gender, and activity level.
    
    CRITICAL INSTRUCTION: 
    Extract the core facts, links, and numbers. Compress them into a maximum of 4 concise bullet points. Avoid filler text.
    ''',
    tools=[google_search]
)

input_form_agent = Agent(
    model='gemini-2.5-flash',
    name='input_form_agent',
    description='Assistant who is specialized in collecting user information.',
    instruction='''
    You are a data collection concierge specialized in fitness metrics.
    Your goal is to ensure we have all required data points before proposing a fitness plan.
    
    REQUIRED FIELDS:
    - weight (current weight)
    - target_weight (goal weight)
    - height
    - age
    - gender
    - activity_level (sedentary, moderate, active, etc.)
    - dietary_preference (vegan, keto, none, etc.)
    
    1. If any information is missing or unclear, ask the user politely to provide it.
    2. Once all fields are gathered, output them clearly as a Markdown list:
       - weight: [value]
       - target_weight: [value]
       - height: [value]
       - age: [value]
       - gender: [value]
       - activity_level: [value]
       - dietary_preference: [value]
    ''',
)

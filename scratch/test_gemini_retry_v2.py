import os
from google.genai import types
from google.adk.models.google_llm import Gemini

def test_gemini_init():
    try:
        # Note: In google-genai, it's 'attempts'
        model = Gemini(
            model_name='gemini-2.5-flash',
            retry_options=types.HttpRetryOptions(initial_delay=1.0, attempts=5)
        )
        print("Gemini init SUCCESS")
    except Exception as e:
        print(f"Gemini init FAILED: {e}")

if __name__ == "__main__":
    test_gemini_init()

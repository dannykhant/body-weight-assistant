from tenacity import retry_if_exception_type, stop_after_attempt, wait_exponential
from google.genai.errors import ClientError

# Common retry configuration for handling 429 Resource Exhausted errors
# multiplier=2, min=4 means it will wait 4s, 8s, 16s, 32s, 60s
RETRY_CONFIG = {
    "retry": retry_if_exception_type(ClientError),
    "stop": stop_after_attempt(5),
    "wait": wait_exponential(multiplier=2, min=4, max=60),
}

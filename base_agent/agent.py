import os
import asyncio
from google.genai import types
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.models.lite_llm import LiteLlm
from langfuse import get_client
from openinference.instrumentation.google_adk import GoogleADKInstrumentor
from google.adk.sessions import InMemorySessionService
 
# Load environment variables from .env file
load_dotenv()

langfuse = get_client()
 
# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

GoogleADKInstrumentor().instrument()

# Ensure the ANTHROPIC_API_KEY is set
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY not found in .env file or environment variables.")

# 1. Define the tools for the agent
def get_weather(location: str) -> str:
    """
    Get the weather for a specific location.

    Args:
        location: The city and state, e.g., San Francisco, CA.
    """
    return f"The weather in {location} is sunny with a high of 75 degrees."

def send_email(to: str, subject: str, body: str) -> str:
    """
    Sends an email to the specified recipient.

    Args:
        to: The email address of the recipient.
        subject: The subject of the email.
        body: The body content of the email.
    """
    print(f"Sending email to: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    return f"Email successfully sent to {to}."

# 4. Create the agent with the defined tools and LLM
root_agent=LlmAgent(
    tools=[get_weather, send_email],
    model=LiteLlm(model="anthropic/claude-haiku-4-5-20251001"),
    name="personal_assistant",
    instruction="You are an assistant.",
)


APP_NAME = "hello_app"
USER_ID = "demo-user"
SESSION_ID = "demo-session"
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    
async def call_agent_in_loop():
    user_msg = types.Content(role="user", parts=[types.Part(text=input("You: "))])
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=user_msg):
        print(f"Agent: {event.content.parts[0].text}")
        user_msg = types.Content(role="user", parts=[types.Part(text=input("You: "))])
        if user_msg.parts[0].text.lower() == "exit":
            print("Ending conversation.")
            break

if __name__ == "__main__":
    asyncio.run(call_agent_in_loop())

import os
from pathlib import Path
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.integrations.langchain import LangchainTool
from langchain_tavily import TavilySearch

# Load .env from the same directory as agent.py
load_dotenv(Path(__file__).with_name(".env"))

# Check Tavily API key
if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY not found in .env file")

# Initialize Tavily Search
tavily_search = TavilySearch(
    max_results=5,
    topic="general"
)

# Convert LangChain tool into ADK-compatible tool
tavily_tool = LangchainTool(tool=tavily_search)

# Create ADK Agent
root_agent = Agent(
    name="root_agent",
    model=LiteLlm(model="groq/openai/gpt-oss-120b"),
    description="A helpful assistant for user questions.",
    instruction="""
    You are a helpful AI assistant with web search capabilities.
    Use Tavily Search whenever the user asks for current information
    or information that requires web research.
    Provide clear and accurate answers based on search results.
    """,
    tools=[tavily_tool],
)

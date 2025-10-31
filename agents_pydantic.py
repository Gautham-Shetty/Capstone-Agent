from pydantic_ai import Agent, WebSearchTool,PromptedOutput
from models import AnswerOutput, InsightOutput
import google.generativeai as genai
import os
from pydantic_ai.toolsets.fastmcp    import FastMCPToolset

from mcp_server import mcp


genai.configure(api_key=os.getenv("API_KEY"))

synthesizer_agent = Agent(
    model="google-gla:gemini-2.5-pro",
    output_type=AnswerOutput,
)

insight_agent = Agent(
    model="google-gla:gemini-2.5-pro",
    output_type=InsightOutput
)

general_knowledge_agent = Agent(
    model="google-gla:gemini-2.5-pro",
    tools=[WebSearchTool] 
)
toolset = FastMCPToolset(client=mcp)

funny_bot_agent = Agent(
    model="google-gla:gemini-2.5-pro",
    toolsets=[toolset],
    system_prompt=(
         "You are FunnyBot"
        "Your ONLY way to tell jokes is by calling the `get_joke` tool by the mcp attached to you.\n"
        "Never invent or write jokes yourself.\n"
        "If you cannot access the tool, say: 'Tool unavailable'."
  
    )
)



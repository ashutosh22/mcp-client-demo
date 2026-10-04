import logging
import os

from langchain_core.runnables import RunnableConfig

#from langchain_anthropic import ChatAnthropic
from src.agent.graph_state import AgentState
from src.client.client import McpClient

from dotenv import load_dotenv

load_dotenv()  # This instantly injects the variables from your .env file into Python's memory


# Core LangChain
from langchain_core import __version__ as core_version
from langchain import __version__ as langchain_version
from langchain.chat_models import init_chat_model

logger = logging.getLogger("mcp-agent.nodes.llm")


logger.info(f"Active LangChain Project: {os.environ.get('LANGCHAIN_PROJECT')}")
logger.info(f"Active LangChain Project: {os.environ.get('LANGCHAIN_API_KEY')}")

logger.info(f"langchain core version: {core_version}")
logger.info(f"langchain langchain version: {langchain_version}")

async def call_model(state: AgentState, config: RunnableConfig) -> dict:
    """The thinking node: queries the LLM with current messages and tools."""
    logger.info("Executing model thinking node...")

    # Extract client injected via context configuration
    mcp_client: McpClient = config["configurable"]["mcp_client"]
    mcp_tools = await mcp_client.list_available_tools()

    # Map MCP tool specs to LangChain tool definition maps
    llm_tools = [
        {
            "name": t.name,
            "description": t.description,
            "input_schema": t.input_schema
        } for t in mcp_tools
    ]

    # Initialize connection and bind tools dynamically
    #model = ChatAnthropic(model="claude-3-5-sonnet-20241022").bind_tools(llm_tools)
    model = init_chat_model(
        model="llama3.2:1b",
        model_provider="ollama",
        temprature=0,
        streaming=False,
        max_retries=3
    ).bind_tools(llm_tools)
    response = await model.ainvoke(state["messages"])

    return {"messages": [response]}

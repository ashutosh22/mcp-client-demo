# src/main.py
import asyncio
import logging

from langchain_core.messages import HumanMessage
from mcp.client.streamable_http import streamable_http_client as http_client

from src.agent.graph import create_agent_graph
from src.client.client import McpClient
from src.config.settings import settings, setup_logging

# Initialize global application-wide logging formats
setup_logging()
logger = logging.getLogger("mcp-agent.main")


async def main():

    logger.info(f"Targeting containerized streamable server at: {settings.SERVER_URL}")

    # 2. Instantiate application core structures
    client = McpClient()
    agent_graph = create_agent_graph()

    try:
        # 3. Boot the background HTTP protocol transport streams
        async with http_client(settings.SERVER_URL) as (read_stream, write_stream):

            # 4. Bind background worker loops inside the client context lifecycle
            async with client.connect_session(read_stream, write_stream):

                # 5. Inject your active client dependency into the execution config map
                config = {"configurable": {"mcp_client": client}}

                # 6. Define the entry payload messages passing into the graph state
                # Inside src/main_agent.py
#                initial_inputs = {
#                    "messages": [
#                        HumanMessage(content=(
#                            "What is the weather forecast for San Francisco, CA? "
#                            "You MUST use the 'get_forecast' tool. "
#                            "Use exactly these numeric values for arguments: latitude=37.7749, longitude=-122.4194. "
#                            "Do not drop the negative sign on the longitude."
#                        ))
#                    ]
#                }

                # Change the query message inside src/main_agent.py:
                initial_inputs = {
                    "messages": [
                        HumanMessage(
                            content="Are there any active weather alerts for California right now? Use the two-letter state code 'CA' with the tools.")
                    ]
                }

                logger.info("Initializing LangGraph async execution stream graph...")
                print("\n🚀 ================= WORKFLOW STARTING =================")

                # 7. Asynchronously stream state changes through nodes as they process data
                async for event in agent_graph.astream(initial_inputs, config=config):
                    for node_name, state_update in event.items():
                        print(f"\n🔹 Node processing finalized: [{node_name}]")

                        # Inspect and display structural messages updated by the node
                        if "messages" in state_update and state_update["messages"]:
                            last_msg = state_update["messages"][-1]

                            # Clean print formatting for different LangChain message types
                            if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                                print(f"   🤖 Assistant Thought: {last_msg.content}")
                                print(f"   🛠️ Requesting Tool Call: {last_msg.tool_calls}")
                            else:
                                print(f"   📄 Content Payload:\n   {last_msg.content}")

                print("\n================= WORKFLOW COMPLETED =================")

    except Exception as e:
        logger.error(f"Critical execution error caught during main application flow: {str(e)}", exc_info=True)


if __name__ == "__main__":
    # Launch async loop engine execution safely
    asyncio.run(main())

import asyncio
import logging
from mcp import ClientSession
# CRITICAL FIX: Import http_client instead of the legacy sse_client
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client as http_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp-weather-client")

# The clean base URL matching your Docker host port mapping
SERVER_URL = "http://127.0.0.1:8081/mcp"


async def run_client():
    logger.info(f"Connecting to containerized streamable server at: {SERVER_URL}")

    try:
        # Establish connection using the correct v2 HTTP client channel
        async with http_client(SERVER_URL) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                logger.info("Initiating connection protocol handshake...")
                await session.initialize()
                logger.info("Handshake verified successfully!")

                # --- Fetch Registered Tools ---
                logger.info("\n--- Fetching Registered Tool Catalog ---")
                tools_response = await session.list_tools()
                for tool in tools_response.tools:
                    print(f"🔹 Found Tool Name: '{tool.name}'")
                    print(f"   Description: {tool.description}\n")

                # --- Call get_forecast Tool ---
                logger.info("--- Invoking 'get_forecast' ---")
                result = await session.call_tool(
                    name="get_forecast",
                    arguments={"latitude": 37.7749, "longitude": -122.4194}
                )
                print("🎯 Response Data:")
                print(result)

    except Exception as e:
        logger.error(f"Connection failure inside client lifecycle: {str(e)}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(run_client())

import asyncio
import logging
from mcp.client.streamable_http import streamable_http_client as http_client
from src.config.settings import settings, setup_logging
from src.client.client import McpClient
from src.models.requests import ForecastRequest

setup_logging()
logger = logging.getLogger("mcp-agent.main")


async def main():
    logger.info(f"Connecting to containerized streamable server at: {settings.SERVER_URL}")
    client = McpClient()

    try:
        # Step 1: Open the HTTP transport layer stream
        async with http_client(settings.SERVER_URL) as (read_stream, write_stream):

            # Step 2: Use the new context manager to safely boot background tasks
            async with client.connect_session(read_stream, write_stream):

                # 3. Extract Tools
                tools = await client.list_available_tools()
                for tool in tools:
                    print(f"🔹 Found Tool Name: '{tool.name}' -> {tool.description}")

                # 3. Request Data Using Validated Model
                payload = ForecastRequest(latitude=37.7749, longitude=-122.4194)
                result = await client.get_forecast(payload)

                print("\n🎯 Response Data:")
                print(result)

    except Exception as e:
        logger.error(f"Connection failure inside client lifecycle: {str(e)}",
                     exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())

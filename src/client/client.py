import logging
from contextlib import asynccontextmanager

from mcp import ClientSession
from mcp.types import CallToolResult

from src.config.settings import settings
from src.models.requests import ForecastRequest, AlertsRequest

logger = logging.getLogger("mcp-agent.client")


class McpClient:
    """Manages connection lifecycles and tool invocations against an MCP Server."""

    def __init__(self):
        self.server_url = settings.SERVER_URL
        self._session: ClientSession | None = None

    @asynccontextmanager
    async def connect_session(self, read_stream, write_stream):
        """Asynchronous context manager that guarantees background dispatcher tasks run first."""
        logger.info("Initializing background protocol session loop...")

        # Wrapping with 'async with' fixes the 'called before run()' error
        async with ClientSession(read_stream, write_stream) as session:
            logger.info("Initiating connection protocol handshake...")
            await session.initialize()
            logger.info("Handshake verified successfully!")

            self._session = session
            try:
                yield self
            finally:
                self._session = None


    async def initialize_session(self, read_stream, write_stream) -> ClientSession:
        """Handles protocol handshaking."""
        logger.info("Initiating connection protocol handshake...")
        session = ClientSession(read_stream, write_stream)
        await session.initialize()
        logger.info("Handshake verified successfully!")
        self._session = session
        return session

    async def list_available_tools(self) -> list:
        """Fetches and displays registered tool catalog."""
        if not self._session:
            raise RuntimeError("Cannot list tools. Client session is not initialized.")

        logger.info("Fetching Registered Tool Catalog...")
        tools_response = await self._session.list_tools()
        return tools_response.tools

    async def get_forecast(self, request_data: ForecastRequest) -> CallToolResult:
        """Safely invokes the forecast tool with a validated request body."""
        if not self._session:
            raise RuntimeError("Cannot execute tool call. Client session is not initialized.")

        logger.info(f"Invoking 'get_forecast' with coordinates: {request_data.model_dump()}")
        result = await self._session.call_tool(
            name="get_forecast",
            arguments=request_data.model_dump()
        )
        return result

    async def get_alerts(self, request_data: AlertsRequest) -> CallToolResult:
        """💡 Invokes the get_alerts tool with a validated request body."""
        if not self._session:
            raise RuntimeError("Cannot execute tool call. Client session is not active.")
        return await self._session.call_tool(name="get_alerts", arguments=request_data.model_dump())
import logging
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig

from src.agent.graph_state import AgentState
from src.client.client import McpClient
from src.models.requests import ForecastRequest, AlertsRequest

logger = logging.getLogger("mcp-agent.nodes.tools")


async def execute_tools(state: AgentState, config: RunnableConfig) -> dict:
    """The action node: routes execution safely through your working McpClient."""
    logger.info("Executing tools action node...")
    mcp_client: McpClient = config["configurable"]["mcp_client"]
    last_message = state["messages"][-1]

    tool_outputs = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        logger.info(f"Invoking tool: '{tool_name}' via MCP infrastructure")

        # Broad exception handler enclosing the dynamic execution lifecycle
        try:
            if tool_name == "get_forecast":
                validated_args = ForecastRequest(**tool_args)
                result = await mcp_client.get_forecast(validated_args)

                # Safely parse the first element from the response content array list
                if result.content and len(result.content) > 0:
                    output_text = result.content[0].text
                else:
                    output_text = "Tool executed successfully but returned empty content."

            # Route 2: Active Alerts Tool
            elif tool_name == "get_alerts":
                validated_args = AlertsRequest(**tool_args)
                result = await mcp_client.get_alerts(validated_args)
                if result.content and len(result.content) > 0:
                    output_text = result.content[0].text
                else:
                    output_text = "Tool executed successfully but returned empty content."
            else:
                output_text = f"Error: Tool '{tool_name}' unknown to orchestration routing layer."

        except Exception as e:
            # Broad exception catch blocks network drops, syntax slips, and parsing failures
            logger.error(f"Broad exception intercepted during tool execution workflow: {str(e)}", exc_info=True)
            output_text = f"Tool failure exception caught: {str(e)}"

        tool_outputs.append(ToolMessage(content=output_text, tool_call_id=tool_id))

    return {"messages": tool_outputs}

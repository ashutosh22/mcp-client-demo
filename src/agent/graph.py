from langgraph.graph import StateGraph, START, END
from src.agent.graph_state import AgentState
from src.agent.nodes.llm_node import call_model
from src.agent.nodes.tool_node import execute_tools


def route_next_node(state: AgentState) -> str:
    """Evaluates whether to continue looping tool actions or finish execution."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "execute_tools"
    return END


def create_agent_graph():
    """Compiles individual node packages and conditional routing paths into a workflow engine."""
    workflow = StateGraph(AgentState)

    # 1. Register clean modular nodes from your subpackage
    workflow.add_node("call_model", call_model)
    workflow.add_node("execute_tools", execute_tools)

    # 2. Establish network workflow directions
    workflow.add_edge(START, "call_model")
    workflow.add_conditional_edges(
        "call_model",
        route_next_node,
        {
            "execute_tools": "execute_tools",
            END: END
        }
    )
    workflow.add_edge("execute_tools", "call_model")

    return workflow.compile()

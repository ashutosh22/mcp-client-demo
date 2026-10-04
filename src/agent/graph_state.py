from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """The production-grade data state passed between nodes."""
    messages: Annotated[Sequence[BaseMessage], add_messages]

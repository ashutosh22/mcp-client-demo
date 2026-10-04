# src/mcp_agent/models/responses.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AgentStep(BaseModel):
    """Tracks a single step of the Agent's thought process."""
    thought: str
    tool_calls_made: List[str] = Field(default_factory=list)

class AgentFinalResponse(BaseModel):
    """The final payload sent back to your application interface."""
    task_id: str
    original_prompt: str
    execution_steps: List[AgentStep] = Field(default_factory=list)
    final_text_answer: str

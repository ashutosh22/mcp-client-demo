# src/mcp_agent/models/alerts.py
from pydantic import BaseModel, Field
from datetime import datetime

class ClientAlert(BaseModel):
    """Encapsulates system execution failures."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    component: str = "McpClient"
    error_message: str

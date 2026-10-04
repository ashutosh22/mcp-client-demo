# src/mcp_agent/models/requests.py
from pydantic import BaseModel, Field

class ForecastRequest(BaseModel):
    """Validates parameters for the weather tool request layer."""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

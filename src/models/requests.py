# src/mcp_agent/models/requests.py
from pydantic import BaseModel, Field

class ForecastRequest(BaseModel):
    """Validates parameters for the weather tool request layer."""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class AlertsRequest(BaseModel):
    """Validates parameters for the state alerts tool request layer."""
    state: str = Field(..., min_length=2, max_length=2)  # Expects 2-letter state code like 'CA'

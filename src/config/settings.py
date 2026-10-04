import logging
import os

class Settings:
    # Look for an environment variable first, fall back to localhost
    SERVER_URL: str = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8081/mcp")
    LOG_LEVEL: int = logging.INFO

settings = Settings()

def setup_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
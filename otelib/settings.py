"""Configuration settings for creating the OTE client."""
from typing import Optional

from pydantic import BaseModel, Field

DEFAULT_HOST = "localhost:8080"


class Settings(BaseModel):
    """Configuration settings for an OTE client."""

    prefix: str = Field("/api/v1", description="Application route prefix.")
    timeout: tuple[float, float] = Field(
        (3.0, 27.0), description="Tuple for URL connect and read timeouts in seconds."
    )

    host: str = Field(
        DEFAULT_HOST, description="Host with oteapi-services up and running."
    )

    class Config:
        """Pydantic configuration class."""

        env_prefix = "OTEAPI_"

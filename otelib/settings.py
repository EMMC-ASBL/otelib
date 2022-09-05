"""Configuration settings for creating the OTE client."""
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Configuration settings for an OTE client."""

    prefix: str = Field("/api/v1", description="Application route prefix.")
    timeout: tuple[float, float] = Field(
        (3.0, 27.0), description="Tuple for URL connect and read timeouts in seconds."
    )

    class Config:
        """Pydantic configuration class."""

        env_prefix = "OTEAPI_"

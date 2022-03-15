"""Configuration settings for creating the OTE client."""
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Configuration settings for an OTE client."""

    prefix: str = Field("/api/v1", description="Application route prefix.")

    class Config:
        """Pydantic configuration class."""

        env_prefix = "OTEAPI_"

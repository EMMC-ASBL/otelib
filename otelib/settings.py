"""Configuration settings for creating the OTE client."""
# pylint: disable=no-name-in-module,too-few-public-methods
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Configuration settings for an OTE client."""

    prefix: str = Field("/api/v1", description="Application route prefix.")

"""Configuration settings for creating the OTE client."""

from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for an OTE client."""

    model_config = SettingsConfigDict(env_prefix="OTEAPI_")

    prefix: Annotated[str, Field(description="Application route prefix.")] = "/api/v1"

    timeout: Annotated[
        tuple[float, float],
        Field(description="Tuple for URL connect and read timeouts in seconds."),
    ] = (3.0, 27.0)

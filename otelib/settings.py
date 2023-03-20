"""Configuration settings for creating the OTE client."""
from pydantic import BaseModel, Field

DEFAULT_HOST = "http://localhost:8080"


class Settings(BaseModel):
    """Configuration settings for an OTE client."""

    prefix: str = Field("/api/v1", description="Application route prefix.")
    timeout: tuple[float, float] = Field(
        (3.0, 27.0), description="Tuple for URL connect and read timeouts in seconds."
    )

    remote_backend: str = Field(
        DEFAULT_HOST,
        description=f"""In case the otelib is supposed to connect to ote-services
        as backend instead of the oteapi-core in the local Python-environment, a host-url
        (included ports) can be set here.
        This might be e.g. {DEFAULT_HOST} (default) or e.g. https://ote.ontotrans.eu""",
    )

    class Config:
        """Pydantic configuration class."""

        env_prefix = "OTEAPI_"

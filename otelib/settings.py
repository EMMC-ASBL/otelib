from pydantic import BaseModel, Field


class Settings(BaseModel):

    prefix: str = Field("/api/v1", description="Application route prefix.")

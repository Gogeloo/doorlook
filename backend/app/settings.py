# Configuration settings using pydantic_settings BaseSettings for environment management
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    title: str = "FastAPI"
    open_ai_api_key: str = "OPEN_AI_API_KEY"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # Set to 'ignore' to allow extra fields that are not defined in the model
    )


settings = Settings()  # type: ignore

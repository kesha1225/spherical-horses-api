from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/spherical_horses"
    )

    app_title: str = "Spherical Horse API"
    app_description: str = "REST API для управления сферическими конями в вакууме"
    app_version: str = "1.0.0"

    debug: bool = False


settings = Settings()

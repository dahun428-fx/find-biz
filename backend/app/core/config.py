from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "find-biz-backend"
    app_env: str = "local"
    app_debug: bool = True
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./backend.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

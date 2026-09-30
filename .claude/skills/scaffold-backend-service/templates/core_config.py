from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./database/dev.db"
    environment: str = "development"
    log_level: str = "INFO"

    # Add this service's own fields here. Secrets (JWT signing keys, API
    # keys) get NO Python-level default — a missing env var should crash
    # startup, not silently run insecure. Check this service's own
    # README.md for which env vars it needs.


settings = Settings()

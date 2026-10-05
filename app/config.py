from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/customer_sync"
    crm_base_url: str = "http://localhost:9000"
    crm_api_key: str = "dev-crm-key"
    webhook_secret: str = "super-secret"
    request_timeout: float = 5.0
    max_retries: int = 3

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "PULSE"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str

    SUPABASE_URL: str
    SUPABASE_KEY: str

    REDIS_URL: str

    SENDGRID_API_KEY: str
    ALERT_FROM_EMAIL: str = "alerts@usepulse.dev"

    FAILURE_THRESHOLD: int = 3 
    CHECK_TIMEOUT_SECONDS: int = 10

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra="ignore"
    )

settings = Settings()
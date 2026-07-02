# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Audit Service"
    API_V1_STR: str = "/api/v1"
    
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    
    # We will get these from the root shared config or env directly
    SUPABASE_URL: str
    SUPABASE_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

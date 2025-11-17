from pydantic_settings import BaseSettings, SettingsConfigDict
import os 

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8'
    )
    
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    REDIS_URL: str = "redis://127.0.0.1:6379/0"
    GEMINI_API_KEY: str
    
    ALGORITHM: str = "HS256"
    
config = Settings()
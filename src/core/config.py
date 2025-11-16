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
    
    ALGORITHM: str = "HS256"
    
config = Settings()
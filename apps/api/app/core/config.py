from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Используем переменную окружения или fallback для разработки
    database_url: str = 'postgresql+asyncpg://postgres:postgres@postgres:5432/ogorod-market'
    
    class Config:
        env_file = '.env'

settings = Settings()
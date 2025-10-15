from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Используем переменную окружения или fallback для разработки
    database_url: str = (
        'postgresql+asyncpg://postgres:postgres@postgres:5432/ogorod-market'
        )
    
    jwt_secret_key: str = 'change-me-in-env'
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60
    
    class Config:
        env_file = '.env'

settings = Settings()
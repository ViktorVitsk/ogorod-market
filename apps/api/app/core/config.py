from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ogorod-market"

    class Config:
        env_file = ".env"

settings = Settings()
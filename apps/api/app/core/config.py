from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_API_ROOT = Path(__file__).resolve().parents[2]
_REPO_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    database_url: str = (
        'postgresql+asyncpg://postgres:postgres@postgres:5432/ogorod-market'
    )
    # No default: a known fallback key would let anyone forge tokens.
    jwt_secret_key: str = Field(min_length=32)
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60
    sql_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=(_API_ROOT / '.env', _REPO_ROOT / '.env'),
        extra='ignore',
    )


settings = Settings()

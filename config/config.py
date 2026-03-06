import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(
        title="Модель пользователя",
        env_file = ".env",
        str_to_lower=True,
        extra='forbid'
    )
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def get_db_url():
        return (
            f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@"
            f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

settings = Settings()


settings = Settings()




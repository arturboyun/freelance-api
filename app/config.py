from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    ENV: str = "local"
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = "02fa26ea8217a726a0639d576ac82892676c39b3c57ed615cf967c5effc37fd4"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    ACCESS_TOKEN_EXPIRE_SECONDS: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    REFRESH_TOKEN_EXPIRE_SECONDS: int = REFRESH_TOKEN_EXPIRE_MINUTES * 60

    COOKIES_SAMESITE: Literal['lax', 'none', 'strict'] = "lax" if ENV == "prod" else "none"

    root_path: Path = Path(__file__).parent.parent.resolve()

    sqlite_path: str = f"sqlite+aiosqlite:///{root_path}/db.sqlite3"
    postgres_path: str = (
        "postgresql+asyncpg://nehz:123qweasdzxc@localhost:5432/freelance-platform"
    )
    redis_url: str = "redis://redis:6379/0"
    db_echo: bool = True


settings = Settings()

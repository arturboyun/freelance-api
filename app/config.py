from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    root_path: Path = Path(__file__).parent.parent.resolve()

    sqlite_path: str = f"sqlite+aiosqlite:///{root_path}/db.sqlite3"
    redis_url: str = "redis://redis:6379/0"
    db_echo: bool = True


settings = Settings()

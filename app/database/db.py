from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings


class DatabaseManager:
    def __init__(self):
        self.engine = create_async_engine(
            settings.sqlite_path, echo=settings.db_echo, future=True
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False, future=True
        )


db_manager = DatabaseManager()

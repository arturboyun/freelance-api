from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import db_manager
from app.logs.repositories.log_repo import LogRepo
from utils.uow.uow_base import IUoW


class SAUoW(IUoW):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        self.log_repo = LogRepo(self.session)
        return self

    async def __aexit__(self, *args):
        await self.close()


async def get_uow() -> SAUoW:
    async with db_manager.session_factory() as session:
        yield SAUoW(session)

from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import db_manager
from app.modules.logs.repositories.log_repo import LogRepo
from app.modules.auth.repositories.auth_repo import AuthRepo
from app.modules.users.repositories.user_repo import UserRepo
from .uow_base import IUoW


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
        self.auth_repo = AuthRepo(self.session)
        self.user_repo = UserRepo(self.session)
        return self

    async def __aexit__(self, *args):
        await self.close()


async def get_uow() -> AsyncIterator[SAUoW]:
    async with db_manager.session_factory() as session:
        yield SAUoW(session)

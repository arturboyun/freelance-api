from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.logs.models import Log
from utils.sqlalchemy.order import get_order_direction


class LogRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        order_by: str = 'created_at',
        order: str = "desc",
        limit: int = 10,
        offset: int = 0,
    ) -> List[Log]:
        order_direction = get_order_direction(order)
        order_by = order_direction(getattr(Log, order_by))
        return list(
            (
                await self.session.execute(
                    select(Log).order_by(order_by).limit(limit).offset(offset)
                )
            ).scalars()
        )

    async def get_by_id(self, _id: int) -> Log:
        return (
            (await self.session.execute(select(Log).where(Log.id == _id)))
            .scalars()
            .first()
        )

    async def find_by(
        self,
        order: str = "desc",
        order_by: str | None = 'created_at',
        limit: int = 700,
        offset: int = 0,
        **kwargs
    ) -> list[Log]:
        order_direction = get_order_direction(order)
        order_by = order_direction(getattr(Log, order_by))

        query = select(Log).order_by(order_by).limit(limit).offset(offset)
        if "created_at__gte" in kwargs:
            query = query.filter(Log.created_at >= kwargs["created_at__gte"])
        return list((await self.session.execute(query)).scalars().all())

    async def create(self, log: dict) -> Log:
        log = Log(**log)
        self.session.add(log)
        return log

    async def delete(self, _id: int) -> None:
        log = await self.get_by_id(_id)
        if log:
            await self.session.delete(log)

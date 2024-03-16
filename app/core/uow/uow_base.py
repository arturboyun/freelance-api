from abc import ABC, abstractmethod
from typing import Any, AsyncContextManager, Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.repositories.auth_repo import AuthRepo
from app.modules.users.repositories.user_repo import UserRepo


class IUoW(ABC):
    auth_repo: AuthRepo
    user_repo: UserRepo
    session: AsyncSession | Any

    # @abstractmethod
    # def __await__(self) -> Awaitable[Any]: ...

    @abstractmethod
    async def __aenter__(self) -> "IUoW": ...

    @abstractmethod
    def __aexit__(self, typ, exc, tb): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...

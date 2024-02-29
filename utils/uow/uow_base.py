from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.logs.repositories.log_repo import LogRepo


class IUoW(ABC):
    log_repo: LogRepo
    session: AsyncSession | Any

    @abstractmethod
    def __aenter__(self): ...

    @abstractmethod
    def __aexit__(self, typ, exc, tb): ...

    @abstractmethod
    def commit(self): ...

    @abstractmethod
    def rollback(self): ...

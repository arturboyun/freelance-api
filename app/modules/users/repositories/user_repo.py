

from sqlalchemy import select
from app.core.repositories.sa_repo_base import SARepoBase
from app.modules.users.models import User
from app.modules.users.schemes import UserCreate, UserUpdate


class UserRepo(SARepoBase[User, UserCreate, UserUpdate]):
    """
    User repository with default methods to Create, Read, Update, Delete.
    
    **Parameters**
    
    * `session`: A SQLAlchemy async session
    * `model`: A SQLAlchemy model class
    """
    def __init__(self, db_session):
        super(UserRepo, self).__init__(db_session, User)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(self.model).where(self.model.username == username)
        return (await self.session.execute(stmt)).scalars().first()
        
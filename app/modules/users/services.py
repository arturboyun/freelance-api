from app.core.uow.uow_base import IUoW
from app.modules.users.schemes import UserDB


class UsersService:
    async def get_user(self, uow: IUoW, id: int) -> UserDB:
        async with uow:
            return UserDB(**(await uow.user_repo.get(id)))

    async def get_user_by_username(self, uow: IUoW, username: str) -> UserDB:
        async with uow:
            user = await uow.user_repo.get_by_username(username)
            return UserDB.parse_obj(user)


def get_users_service() -> UsersService:
    return UsersService()

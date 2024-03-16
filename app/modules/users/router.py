from typing import Annotated
from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.core.uow.sqlalchemy_uow import SAUoW, get_uow
from app.core.uow.uow_base import IUoW

from app.modules.users.schemes import UserDB
from app.modules.users.services import UsersService, get_users_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserDB)
async def read_users_me(
    current_user: Annotated[str, Depends(get_current_user)],
    uow: Annotated[SAUoW, Depends(get_uow)],
    service: Annotated[UsersService, Depends(get_users_service)]
) -> UserDB:
    return await service.get_user_by_username(uow, current_user)

from typing import Annotated

from fastapi import APIRouter, Depends

from app.logs.services import LogService
from app.schemes import LogCreate, LogDB
from utils.uow.sqlalchemy_uow import SAUoW, get_uow

router = APIRouter(prefix="/log")


@router.post("/", response_model=LogDB)
async def save_log(
    log: LogCreate,
    uow: Annotated[SAUoW, Depends(get_uow)],
) -> LogDB:
    return await LogService().add_log(uow, log)


@router.get("/", response_model=list[LogDB])
async def get_last_hour_logs(
    uow: Annotated[SAUoW, Depends(get_uow)],
) -> list[LogDB]:
    return await LogService().get_last_hour_logs(uow)

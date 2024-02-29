import datetime

from app.schemes import LogCreate, LogDB
from utils.uow.uow_base import IUoW


class LogService:

    async def add_log(self, uow: IUoW, log: LogCreate) -> LogDB:
        log_dict = log.model_dump()
        async with uow:
            log_created = await uow.log_repo.create(log_dict)
            await uow.commit()
            await uow.session.refresh(log_created)
            return LogDB.parse_obj(log_created)

    async def get_last_hour_logs(self, uow: IUoW) -> list[LogDB]:
        now = datetime.datetime.utcnow()
        last_hour = now - datetime.timedelta(hours=1)
        async with uow:
            last_hour_logs = await uow.log_repo.find_by(uow, created_at__gte=last_hour)
            return [LogDB.parse_obj(log) for log in last_hour_logs]

import datetime

from pydantic import BaseModel


class LogBase(BaseModel):
    service_name: str
    environment: str
    endpoint: str
    traceback: str
    exception_type: str | None = None


class LogCreate(LogBase):
    service_name: str
    environment: str
    endpoint: str
    traceback: str
    exception_type: str | None = None


class LogUpdate(LogBase):
    service_name: str | None = None
    environment: str | None = None
    endpoint: str | None = None
    traceback: str | None = None
    exception_type: str | None = None


class LogInDBBase(LogBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class LogDB(LogInDBBase):
    pass

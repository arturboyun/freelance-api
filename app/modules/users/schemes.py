import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str | None = None
    password: str | None = None


class UserCreate(UserBase):
    username: str
    password: str


class UserUpdate(UserBase):
    ...


class UserInDBBase(BaseModel):
    id: int
    username: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class UserDB(UserInDBBase):
    ...

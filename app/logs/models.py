import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Log(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column()
    environment: Mapped[str] = mapped_column()
    endpoint: Mapped[str] = mapped_column()
    traceback: Mapped[str] = mapped_column()
    exception_type: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=func.current_timestamp()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

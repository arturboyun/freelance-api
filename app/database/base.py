from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

DeclarativeBase = declarative_base(metadata=metadata)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    def __init_subclass__(cls, **kwargs):
        if not cls.__dict__.get("__tablename__", None):
            cls.__tablename__ = cls.__name__.lower()
        super().__init_subclass__(**kwargs)

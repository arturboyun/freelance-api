from typing import Any, Generic, Sequence, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SARepoBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        """
        Repo object with default methods to Create, Read, Update, Delete.

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `session`: A SQLAlchemy async session
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.session = session

    async def get(self, id: int) -> type[ModelType] | None:
        """
        Get a single record by id.

        **Parameters**

        * `id`: The record's id

        **Returns**

        * A single record
        """
        return (
            (await self.session.execute(select(self.model).where(self.model.id == id)))
            .scalars()
            .first()
        )
    
    async def create(self, schema: CreateSchemaType) -> type[ModelType]:
        """
        Create a new record.

        **Parameters**

        * `schema`: A Pydantic model (schema) instance

        **Returns**

        * The created record
        """
        record = self.model(**schema.model_dump())
        self.session.add(record)
        return record
    
    async def update(self, id: int, schema: UpdateSchemaType) -> type[ModelType] | None:
        """
        Update a record by id.

        **Parameters**

        * `id`: The record's id
        * `schema`: A Pydantic model (schema) instance

        **Returns**

        * The updated record
        """
        record = await self.get(id)
        if record:
            for field, value in schema:
                setattr(record, field, value)
            return record
        
    async def delete(self, id: int) -> type[ModelType] | None:
        """
        Delete a record by id.

        **Parameters**

        * `id`: The record's id

        **Returns**

        * The deleted record
        """
        record = await self.get(id)
        if record:
            await self.session.delete(record)
            return record

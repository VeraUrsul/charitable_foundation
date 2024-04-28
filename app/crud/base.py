from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(
        self,
        model: Type[ModelType]
    ):
        self.model = model

    async def get(
        self,
        object_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        db_object = await session.execute(
            select(self.model).where(self.model.id == object_id)
        )
        return db_object.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ) -> List[ModelType]:
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def get_not_closed(self, session: AsyncSession):
        db_objects = await session.execute(
            select(self.model).where(~self.model.fully_invested).order_by(
                self.model.create_date
            )
        )
        return db_objects.scalars().all()

    async def create(
        self,
        object_in: CreateSchemaType,
        session: AsyncSession,
        user: Optional[User] = None,
        need_commit: bool = True
    ) -> ModelType:
        object_in_data = object_in.dict()
        if user:
            object_in_data['user_id'] = user.id
        object_in_data['invested_amount'] = 0
        db_object = self.model(**object_in_data)
        session.add(db_object)
        if need_commit:
            await session.commit()
            await session.refresh(db_object)
        return db_object

    async def update(
        self,
        db_object: ModelType,
        object_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def remove(
        self,
        db_object: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        await session.delete(db_object)
        await session.commit()
        return db_object

    async def get_not_fully_invested_object(
        self,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        db_object = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 0
            ).order_by(self.model.create_date.asc())
        )
        return db_object.scalars().all()

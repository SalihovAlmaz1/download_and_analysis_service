from typing import Generic, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.base_repository import AbstractRepository, ModelType

class SQLAlchemyRepository(AbstractRepository[ModelType], Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> ModelType:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(self, pk: int, **kwargs) -> ModelType | None:
        obj = await self.get_single(pk)
        if obj is None:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await self.session.flush()
        return obj

    async def delete(self, pk: int) -> None:
        obj = await self.get_single(pk)
        if obj is not None:
            await self.session.delete(obj)
            await self.session.flush()

    async def get_single(self, pk: int) -> ModelType | None:
        return await self.session.get(self.model, pk)

    async def list(self, *, limit: int, offset: int) -> list[ModelType]:
        result = await self.session.execute(
            select(self.model).order_by(self.model.id).limit(limit).offset(offset)
        )
        return list(result.scalars().all())
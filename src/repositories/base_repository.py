from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ModelType = TypeVar("ModelType")


class AbstractRepository(ABC, Generic[ModelType]):

    @abstractmethod
    async def create(self, **kwargs) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def update(self, pk: int, **kwargs) -> ModelType | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, pk: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_single(self, pk: int) -> ModelType | None:
        raise NotImplementedError

    @abstractmethod
    async def list(self, *, limit: int, offset: int) -> list[ModelType]:
        raise NotImplementedError
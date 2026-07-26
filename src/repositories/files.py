from sqlalchemy import func, select, desc, asc

from src.models.files import File
from src.repositories.sqlalchemy_repository import SQLAlchemyRepository


class FileRepository(SQLAlchemyRepository[File]):
    model = File

    async def get_by_filename(self, filename: str) -> File | None:
        result = await self.session.execute(
            select(File).where(File.filename == filename)
        )
        return result.scalar_one_or_none()

    async def list_by_downloaded_at(
        self, *, limit: int, offset: int, order: str = "desc"
    ) -> list[File]:
        direction = desc if order == "desc" else asc
        result = await self.session.execute(
            select(File).order_by(direction(File.downloaded_at)).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_all(self) -> list[File]:
        result = await self.session.execute(select(File).order_by(File.downloaded_at.desc()))
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(File))
        return result.scalar_one()

    async def get_many_by_ids(self, ids: list[int]) -> list[File]:
        result = await self.session.execute(select(File).where(File.id.in_(ids)))
        return list(result.scalars().all())
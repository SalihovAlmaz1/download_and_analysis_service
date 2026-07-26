from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database.db_helper import db_helper
from src.repositories.files import FileRepository

async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with db_helper.get_db_session() as session:
        yield session

def get_file_repository(session: AsyncSession = Depends(get_db_session)) -> FileRepository:
    return FileRepository(session)
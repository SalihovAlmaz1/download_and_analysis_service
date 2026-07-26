from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from config.database.db_helper import db_helper
from config.project_config import settings
from src.core.progress import DownloadProgressTracker
from src.models.base_model import Base
from src.services.api_client import FilesApiClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    client = httpx.AsyncClient(
        base_url=settings.BASE_URL,
        headers={
            "X-Candidate-Id": settings.CANDIDATE_ID,
        },
    )
    app.state.api = FilesApiClient(client)
    app.state.download_progress = DownloadProgressTracker()
    yield

    await client.aclose()
from fastapi import APIRouter

from src.routes.download import router as download_router
from src.routes.files import router as files_router


def get_apps_router() -> APIRouter:
    router = APIRouter()
    router.include_router(download_router, prefix="/api/download", tags=["Download"])
    router.include_router(files_router, prefix="/api/files", tags=["Files"])
    return router
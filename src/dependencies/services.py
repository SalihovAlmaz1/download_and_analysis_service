from fastapi import Request

from config.database.db_config import settings_db
from config.database.db_helper import db_helper
from src.core.progress import DownloadProgressTracker
from src.services.files import DownloadService
from src.services.storage import FileStorage

def get_storage():
    return FileStorage(settings_db.STORAGE_DIR)

def get_progress_tracker(request: Request) -> DownloadProgressTracker:
    return request.app.state.download_progress


def get_download_service(request: Request) -> DownloadService:
    return DownloadService(
        api_client=request.app.state.api,
        storage=get_storage(),
        db_helper=db_helper,
        progress=request.app.state.download_progress,
    )
from dataclasses import asdict

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from src.core.progress import DownloadProgressTracker, DownloadStatus
from src.dependencies.services import get_download_service, get_progress_tracker
from src.services.files import DownloadService

router = APIRouter()


@router.post("/start")
async def start_download(
    background_tasks: BackgroundTasks,
    service: DownloadService = Depends(get_download_service),
):
    if service.progress.snapshot().status == DownloadStatus.RUNNING:
        raise HTTPException(status_code=409)

    background_tasks.add_task(service.download_all)
    return {"status": "started"}


@router.get("/status")
async def get_download_status(
    progress: DownloadProgressTracker = Depends(get_progress_tracker),
):
    return asdict(progress.snapshot())
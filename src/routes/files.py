from fastapi import APIRouter, Depends, HTTPException, Query

from src.dependencies.db import get_file_repository
from src.dependencies.services import get_storage
from src.repositories.files import FileRepository
from src.schemas.files import AnalysisResult, AnalyzeRequest, FileOut, PaginatedFiles
from src.services.analysis import AnalysisService
from src.services.storage import FileStorage

router = APIRouter()


@router.get("", response_model=PaginatedFiles)
async def list_files(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    repository: FileRepository = Depends(get_file_repository),
):
    offset = (page - 1) * page_size
    items = await repository.list_by_downloaded_at(limit=page_size, offset=offset, order=order)
    total = await repository.count()
    return PaginatedFiles(
        items=[FileOut.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_files(
    payload: AnalyzeRequest,
    repository: FileRepository = Depends(get_file_repository),
    storage: FileStorage = Depends(get_storage),
):
    files = await repository.get_all() if payload.select_all else await repository.get_many_by_ids(payload.file_ids)

    if not files:
        raise HTTPException(status_code=404)

    return await AnalysisService(storage).analyze(files)
from datetime import datetime

from pydantic import BaseModel, model_validator


class FileOut(BaseModel):
    id: int
    filename: str
    downloaded_at: datetime

    model_config = {"from_attributes": True}


class PaginatedFiles(BaseModel):
    items: list[FileOut]
    total: int
    page: int
    page_size: int


class AnalyzeRequest(BaseModel):
    file_ids: list[int] | None = None
    select_all: bool = False

    @model_validator(mode="after")
    def check_selection(self):
        if not self.select_all and not self.file_ids:
            raise ValueError("Или id-шники, или select_all")
        return self


class FileDigitStats(BaseModel):
    file_id: int
    filename: str
    counts: dict[str, int]


class AnalysisResult(BaseModel):
    total: dict[str, int]
    per_file: list[FileDigitStats]
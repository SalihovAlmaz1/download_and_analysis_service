from collections import Counter

from src.models.files import File
from src.schemas.files import AnalysisResult, FileDigitStats
from src.services.storage import FileStorage

DIGITS = [str(d) for d in range(10)]


def _normalize(counter: Counter) -> dict[str, int]:
    return {digit: counter.get(digit, 0) for digit in DIGITS}


class AnalysisService:
    def __init__(self, storage: FileStorage):
        self.storage = storage

    async def analyze(self, files: list[File]) -> AnalysisResult:
        total_counter: Counter = Counter()
        per_file: list[FileDigitStats] = []

        for file in files:
            content = await self.storage.read(file.filename)
            file_counter = Counter(ch for ch in content.decode("utf-8") if ch.isdigit())
            total_counter.update(file_counter)
            per_file.append(
                FileDigitStats(file_id=file.id, filename=file.filename, counts=_normalize(file_counter))
            )

        return AnalysisResult(total=_normalize(total_counter), per_file=per_file)
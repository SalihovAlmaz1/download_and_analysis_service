from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class DownloadStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


@dataclass
class DownloadProgress:
    status: DownloadStatus = DownloadStatus.IDLE
    started_at: datetime | None = None
    finished_at: datetime | None = None
    total_seen: int = 0
    downloaded: int = 0
    error: str | None = None


class DownloadProgressTracker:
    def __init__(self) -> None:
        self._state = DownloadProgress()

    def snapshot(self) -> DownloadProgress:
        return self._state

    def start(self) -> None:
        self._state = DownloadProgress(
            status=DownloadStatus.RUNNING, started_at=datetime.now(timezone.utc)
        )

    def add_batch(self, count: int) -> None:
        self._state.total_seen += count

    def mark_downloaded(self, count: int) -> None:
        self._state.downloaded += count

    def finish(self) -> None:
        self._state.status = DownloadStatus.DONE
        self._state.finished_at = datetime.now(timezone.utc)

    def fail(self, error: str) -> None:
        self._state.status = DownloadStatus.ERROR
        self._state.error = error
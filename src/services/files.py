import zipfile
from datetime import datetime, timezone
from io import BytesIO

from config.database.db_helper import DatabaseHelper
from src.core.progress import DownloadProgressTracker
from src.repositories.files import FileRepository
from src.services.api_client import FilesApiClient
from src.services.storage import FileStorage
CHUNK_SIZE = 3
class DownloadService:
    def __init__(
        self,
        api_client: FilesApiClient,
        storage: FileStorage,
        db_helper: DatabaseHelper,
        progress: DownloadProgressTracker,
    ):
        self.api_client = api_client
        self.storage = storage
        self.db_helper = db_helper
        self.progress = progress

    async def download_all(self) -> None:
        self.progress.start()
        try:
            while True:
                names = await self.api_client.get_names()
                if not names:
                    break

                self.progress.add_batch(len(names))

                for i in range(0, len(names), CHUNK_SIZE):
                    chunk = names[i : i + CHUNK_SIZE]
                    archive_bytes = await self.api_client.download(chunk)
                    saved_names = await self._extract_and_save(archive_bytes)
                    await self.api_client.mark_downloaded(saved_names)
                    self.progress.mark_downloaded(len(saved_names))
        except Exception as error:
            self.progress.fail(str(error))
            raise
        else:
            self.progress.finish()

    async def _extract_and_save(self, archive_bytes: bytes) -> list[str]:
        saved_names: list[str] = []
        async with self.db_helper.get_db_session() as session:
            repository = FileRepository(session)
            with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
                for filename in archive.namelist():
                    content = archive.read(filename)
                    path = await self.storage.save(filename, content)

                    existing = await repository.get_by_filename(filename)
                    if existing is None:
                        await repository.create(
                            filename=filename,
                            path=str(path),
                            downloaded_at=datetime.now(timezone.utc),
                        )
                    saved_names.append(filename)
            await session.commit()
        return saved_names
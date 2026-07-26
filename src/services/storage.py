from pathlib import Path
import aiofiles

class FileStorage:

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    async def save(self, filename: str, content: bytes) -> Path:
        path = self.root / filename

        async with aiofiles.open(path,"wb") as file:
            await file.write(content)

        return path

    async def read(self, filename:str) -> bytes:
        path = self.root / filename

        async with aiofiles.open(path, "rb") as file:
            return await file.read()

    def path(self, filename: str) -> Path:
        return self.root / filename
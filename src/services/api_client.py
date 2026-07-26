import asyncio

import httpx

DEFAULT_RETRY_SECONDS = 1
MAX_RETRIES = 30


class FilesApiClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        for _ in range(MAX_RETRIES):
            response = await self.client.request(method, url, **kwargs)

            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", DEFAULT_RETRY_SECONDS))
                await asyncio.sleep(retry_after)
                continue

            if response.status_code == 403:
                retry_after = response.headers.get("Retry-After")
                if retry_after is not None:
                    await asyncio.sleep(int(retry_after))
                    continue

            response.raise_for_status()
            return response

        raise RuntimeError(f"Exceeded {MAX_RETRIES} retries for {method} {url}")

    async def get_names(self) -> list[str]:
        response = await self._request(
            "GET",
            "/api/files/names"
        )
        return response.json()["file_names"]

    async def download(self, file_names: list[str]):
        if len(file_names) > 3:
            raise ValueError("API позволяет скачать только 3 файла за один запрос")
        response = await self._request(
            "POST", "/api/files/download", json={"file_names": file_names}
        )
        return response.content

    async def mark_downloaded(self, file_names: list[str]) -> dict:
        response = await self._request(
            "POST", "/api/files/downloaded", json={"file_names": file_names}
        )
        return response.json()
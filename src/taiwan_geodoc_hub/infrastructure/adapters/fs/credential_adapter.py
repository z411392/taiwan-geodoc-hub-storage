from taiwan_geodoc_hub.modules.access_managing.domain.ports.credential_repository import (
    CredentialRepository,
)
from taiwan_geodoc_hub.modules.access_managing.dtos.credentials import (
    Credentials,
)
from typing import Optional
from json import loads, dumps
from os.path import exists
import aiofiles


class CredentialAdapter(CredentialRepository):
    _credentials_path: str = "credentials.json"

    async def load(self) -> Optional[Credentials]:
        if not exists(self._credentials_path):
            return None
        async with aiofiles.open(self._credentials_path, "r", encoding="utf-8") as file:
            data = await file.read()
            return Credentials(**loads(data))

    async def save(self, credential: Credentials):
        async with aiofiles.open(self._credentials_path, "w", encoding="utf-8") as file:
            await file.write(dumps(credential, indent=4, ensure_ascii=False))

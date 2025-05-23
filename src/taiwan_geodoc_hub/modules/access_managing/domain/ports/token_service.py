from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.access_managing.dtos.credentials import (
    Credentials,
)
from typing import Optional, Awaitable


class TokenService(ABC):
    @abstractmethod
    async def refresh_token(
        self, refresh_token: str
    ) -> Awaitable[Optional[Credentials]]:
        raise NotImplementedError

    @abstractmethod
    def is_token_valid(self, id_token: str) -> bool:
        raise NotImplementedError

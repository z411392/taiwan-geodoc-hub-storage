from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.access_managing.dtos.credentials import (
    Credentials,
)
from typing import Optional, Awaitable


class CredentialRepository(ABC):
    @abstractmethod
    def load(self) -> Awaitable[Optional[Credentials]]:
        raise NotImplementedError

    @abstractmethod
    def save(self, credential: Credentials) -> Awaitable[None]:
        raise NotImplementedError

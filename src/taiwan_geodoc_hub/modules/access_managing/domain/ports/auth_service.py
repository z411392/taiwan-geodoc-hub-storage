from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.access_managing.dtos.credentials import (
    Credentials,
)
from typing import Awaitable


class AuthService(ABC):
    @abstractmethod
    def auth(self) -> Awaitable[Credentials]:
        raise NotImplementedError

from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.registration_managing.dtos.registration import (
    Registration,
)
from typing import Generic, TypeVar, Any, Awaitable

T = TypeVar("T", bound=Any)


class RegistrationRepository(ABC, Generic[T]):
    @abstractmethod
    def exists(self, registration_id: str, /, uow: T) -> Awaitable[bool]:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        registration_id: str,
        data: Registration,
        /,
        uow: T,
    ) -> Awaitable[None]:
        raise NotImplementedError

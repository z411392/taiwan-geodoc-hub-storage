from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.registration_managing.dtos.snapshot import (
    Snapshot,
)
from typing import Generic, TypeVar, Any, Awaitable

T = TypeVar("T", bound=Any)


class SnapshotRepository(ABC, Generic[T]):
    @abstractmethod
    def exists(
        self,
        snapshot_id: str,
        /,
        uow: T,
    ) -> Awaitable[bool]:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        snapshot_id: str,
        data: Snapshot,
        /,
        uow: T,
    ) -> Awaitable[None]:
        raise NotImplementedError

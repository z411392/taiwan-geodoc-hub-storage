from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Awaitable
from taiwan_geodoc_hub.modules.system_maintaining.domain.process_managers.projecting_process_manager import (
    ProjectingProcessManager,
)

T = TypeVar("T", bound=Any)


class ProcessManagerRepository(ABC, Generic[T]):
    @abstractmethod
    def load(
        self,
        trace_id: str,
        /,
        uow: T,
    ) -> Awaitable[ProjectingProcessManager]:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        trace_id: str,
        process_manager: ProjectingProcessManager,
        /,
        uow: T,
    ) -> Awaitable[None]:
        raise NotImplementedError

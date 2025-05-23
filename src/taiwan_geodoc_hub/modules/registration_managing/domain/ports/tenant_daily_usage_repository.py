from abc import ABC, abstractmethod
from taiwan_geodoc_hub.modules.registration_managing.dtos.tenant_daily_usage import (
    TenantDailyUsage,
)
from typing import Generic, TypeVar, Any, Awaitable, Optional

T = TypeVar("T", bound=Any)


class TenantDailyUsageRepository(ABC, Generic[T]):
    @abstractmethod
    def load(
        self,
        date: str,
        /,
        uow: T,
    ) -> Awaitable[Optional[TenantDailyUsage]]:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        date: str,
        data: TenantDailyUsage,
        /,
        uow: T,
    ) -> Awaitable[None]:
        raise NotImplementedError

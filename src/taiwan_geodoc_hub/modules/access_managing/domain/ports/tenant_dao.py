from abc import ABC, abstractmethod
from typing import Optional, Awaitable, List
from taiwan_geodoc_hub.modules.access_managing.dtos.tenant import Tenant


class TenantDao(ABC):
    @abstractmethod
    def in_ids(self, *tenant_ids: List[str]) -> Awaitable[List[Tenant]]:
        raise NotImplementedError

    @abstractmethod
    def by_id(self, tenant_id: str) -> Awaitable[Optional[Tenant]]:
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import Optional, Awaitable, List
from taiwan_geodoc_hub.modules.access_managing.dtos.role import Role


class RoleDao(ABC):
    @abstractmethod
    def in_ids(self, *user_ids: List[str]) -> Awaitable[List[Role]]:
        raise NotImplementedError

    @abstractmethod
    def by_id(self, user_id: str) -> Awaitable[Optional[Role]]:
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import Optional, Awaitable, List
from firebase_admin.auth import UserRecord


class UserDao(ABC):
    @abstractmethod
    def in_ids(self, *user_id: List[str]) -> Awaitable[List[UserRecord]]:
        raise NotImplementedError

    @abstractmethod
    def by_id(self, user_id: str) -> Awaitable[Optional[UserRecord]]:
        raise NotImplementedError

    @abstractmethod
    def from_id_token(self, id_token: str) -> Awaitable[Optional[UserRecord]]:
        raise NotImplementedError

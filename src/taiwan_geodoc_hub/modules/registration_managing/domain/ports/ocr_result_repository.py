from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Optional, Awaitable

T = TypeVar("T", bound=Any)


class OCRResultRepository(ABC, Generic[T]):
    @abstractmethod
    def load(self, ocr_result_id: str, uow: T) -> Awaitable[Optional[str]]:
        raise NotImplementedError

    @abstractmethod
    def save(self, ocr_result_id: str, text: str, uow: T) -> Awaitable[None]:
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import Awaitable


class OCRService(ABC):
    @abstractmethod
    def __call__(self, image: bytes, language: str = "cht") -> Awaitable[str]:
        raise NotImplementedError

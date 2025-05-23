from injector import inject
from google.cloud.firestore import AsyncClient, async_transactional, AsyncTransaction
from typing import (
    Protocol,
    runtime_checkable,
    Awaitable,
    TypeVar,
    Generic,
    Any,
    Callable,
)
from functools import wraps

T = TypeVar("T", bound=Any)


@runtime_checkable
class Repository(Protocol):
    def load(self, key: str, *, uow: AsyncTransaction) -> Awaitable[T]: ...
    def save(self, key: str, data: T, *, uow: AsyncTransaction) -> Awaitable[T]: ...


@runtime_checkable
class CacheKeyComputer(Protocol):
    def __call__(self, *args, **kwargs) -> Awaitable[str]: ...


class ReadThroughCachePolicy(Generic[T]):
    _db: AsyncClient

    @inject
    def __init__(
        self,
        /,
        db: AsyncClient,
    ):
        self._db = db

    def __call__(
        self,
        func: Callable[..., Awaitable[None]],
        /,
        repository: Repository,
        compute_key: CacheKeyComputer,
    ):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            key = await compute_key(*args, **kwargs)

            @async_transactional
            async def run_in_transaction(transaction: AsyncTransaction):
                hit = await repository.load(key, uow=transaction)
                if hit is not None:
                    return hit

                data = await func(*args, **kwargs)

                await repository.load(key, data, uow=transaction)

                return data

            data = await run_in_transaction(self._db.transaction())
            return data

        return wrapped

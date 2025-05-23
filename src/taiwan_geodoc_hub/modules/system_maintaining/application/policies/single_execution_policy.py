from google.cloud.firestore import AsyncClient, AsyncTransaction, async_transactional
from taiwan_geodoc_hub.modules.system_maintaining.events.execution_completed import (
    ExecutionCompleted,
)
from taiwan_geodoc_hub.modules.system_maintaining.events.execution_failed import (
    ExecutionFailed,
)
from typing import Callable, Awaitable
from taiwan_geodoc_hub.modules.system_maintaining.domain.ports.process_manager_repository import (
    ProcessManagerRepository,
)
from taiwan_geodoc_hub.infrastructure.constants.tokens import TraceId
from injector import inject
from functools import wraps


class SingleExecutionPolicy:
    _db: AsyncClient
    _process_manager_repository: ProcessManagerRepository
    _trace_id: str

    @inject
    def __init__(
        self,
        /,
        db: AsyncClient,
        process_manager_repository: ProcessManagerRepository,
        trace_id: TraceId,
    ):
        self._db = db
        self._process_manager_repository = process_manager_repository
        self._trace_id = trace_id

    def __call__(self, func: Callable[..., Awaitable[None]]):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            @async_transactional
            async def run_in_transaction(transaction: AsyncTransaction):
                process_manager = await self._process_manager_repository.load(
                    self._trace_id,
                    uow=transaction,
                )
                try:
                    await func(*args, **kwargs)
                    await process_manager.add(ExecutionCompleted())
                    await self._process_manager_repository.save(
                        self._trace_id,
                        process_manager,
                        uow=transaction,
                    )
                    return None
                except Exception as exception:
                    await process_manager.add(ExecutionFailed(reason=str(exception)))
                    await self._process_manager_repository.save(
                        self._trace_id,
                        process_manager,
                        uow=transaction,
                    )
                    return exception

            exception_raised = await run_in_transaction(self._db.transaction())
            if exception_raised:
                raise exception_raised

        return wrapped

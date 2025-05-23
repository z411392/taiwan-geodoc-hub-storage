from google.cloud.firestore import (
    AsyncClient,
    AsyncCollectionReference,
    AsyncTransaction,
)
from taiwan_geodoc_hub.infrastructure.types.collection import (
    Collection,
)
from injector import inject
from typing import Awaitable
from taiwan_geodoc_hub.modules.system_maintaining.domain.ports.process_manager_repository import (
    ProcessManagerRepository,
)
from taiwan_geodoc_hub.modules.system_maintaining.domain.process_managers.projecting_process_manager import (
    ProjectingProcessManager,
    Completed,
    Failed,
    Progressing,
)
from datetime import datetime, timedelta, UTC


class ProcessManagerAdapter(ProcessManagerRepository[AsyncTransaction]):
    _collection: AsyncCollectionReference

    @inject
    def __init__(self, /, db: AsyncClient):
        self._collection = db.collection(str(Collection.Processes))

    async def load(
        self,
        trace_id: str,
        /,
        uow: AsyncTransaction,
    ):
        document = self._collection.document(trace_id)
        db: AsyncClient = uow._client
        document_snapshot = await anext(aiter(db.get_all([document], transaction=uow)))
        if document_snapshot.exists:
            data = document_snapshot.to_dict()
            if data["status"] == Progressing.status:
                return ProjectingProcessManager(Progressing.from_dict(data))
            if data["status"] == Completed.status:
                return ProjectingProcessManager(Completed.from_dict(data))
            if data["status"] == Failed.status:
                return ProjectingProcessManager(Failed.from_dict(data))
        return ProjectingProcessManager(Progressing())

    async def save(
        self,
        trace_id: str,
        process_manager: ProjectingProcessManager,
        /,
        uow: AsyncTransaction,
    ) -> Awaitable[None]:
        document = self._collection.document(trace_id)
        data = process_manager.state.to_dict()
        if data.get("expiredAt") is None:
            expired_at = datetime.now(UTC) + timedelta(minutes=10)
            data.update(
                expiredAt=expired_at,
            )
        uow.set(
            document,
            data,
            merge=True,
        )

from google.cloud.firestore import (
    AsyncClient,
    AsyncCollectionReference,
    AsyncTransaction,
)
from taiwan_geodoc_hub.infrastructure.constants.collections import (
    Collections,
)
from taiwan_geodoc_hub.infrastructure.constants.types import (
    TenantId,
)
from injector import inject
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.snapshot_repository import (
    SnapshotRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.snapshot import (
    Snapshot,
)
from typing import Awaitable


class SnapshotAdapter(SnapshotRepository[AsyncTransaction]):
    _collection: AsyncCollectionReference

    @inject
    def __init__(self, db: AsyncClient, tenant_id: TenantId):
        self._collection = db.collection(
            str(Collections.snapshots).replace(":tenantId", tenant_id)
        )

    async def exists(
        self,
        snapshot_id: str,
        /,
        uow: AsyncTransaction,
    ) -> Awaitable[bool]:
        document = self._collection.document(snapshot_id)
        db: AsyncClient = uow._client
        document_snapshot = await anext(aiter(db.get_all([document], transaction=uow)))
        return document_snapshot.exists

    async def save(
        self,
        snapshot_id: str,
        data: Snapshot,
        /,
        uow: AsyncTransaction,
    ) -> Awaitable[None]:
        document = self._collection.document(snapshot_id)
        snapshot: Snapshot = {k: v for k, v in data.items() if k not in ("id")}
        uow.set(
            document,
            snapshot,
            merge=True,
        )

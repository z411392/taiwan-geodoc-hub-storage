from google.cloud.firestore import (
    AsyncClient,
    AsyncCollectionReference,
    AsyncTransaction,
)
from taiwan_geodoc_hub.infrastructure.types.collection import (
    Collection,
)
from injector import inject
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.snapshot_repository import (
    SnapshotRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.snapshot import (
    Snapshot,
)


class SnapshotAdapter(SnapshotRepository[AsyncTransaction]):
    _collection: AsyncCollectionReference

    @inject
    def __init__(self, /, db: AsyncClient):
        self._collection = db.collection(str(Collection.Snapshots))

    async def exists(
        self,
        snapshot_id: str,
        /,
        uow: AsyncTransaction,
    ):
        document = self._collection.document(snapshot_id)
        db: AsyncClient = uow._client
        document_snapshot = await anext(aiter(db.get_all([document], transaction=uow)))
        return document_snapshot.exists

    async def save(
        self,
        snapshot_id: str,
        snapshot: Snapshot,
        /,
        uow: AsyncTransaction,
    ):
        document = self._collection.document(snapshot_id)
        data = {k: v for k, v in snapshot.items() if k not in ("id")}
        uow.set(
            document,
            data,
            merge=True,
        )

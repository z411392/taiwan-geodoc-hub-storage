from google.cloud.firestore import (
    AsyncClient,
    AsyncCollectionReference,
    AsyncTransaction,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.registration_repository import (
    RegistrationRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.registration import (
    Registration,
)
from taiwan_geodoc_hub.infrastructure.types.collection import (
    Collection,
)
from taiwan_geodoc_hub.infrastructure.constants.tokens import (
    SnapshotId,
)
from injector import inject


class RegistrationAdapter(RegistrationRepository[AsyncTransaction]):
    _collection: AsyncCollectionReference

    @inject
    def __init__(self, /, db: AsyncClient, snapshot_id: SnapshotId):
        self._collection = db.collection(
            str(Collection.Registrations).replace(":snapshotId", snapshot_id)
        )

    async def exists(self, registration_id: str, /, uow: AsyncTransaction):
        document = self._collection.document(registration_id)
        db: AsyncClient = uow._client
        document_snapshot = await anext(aiter(db.get_all([document], transaction=uow)))
        return document_snapshot.exists

    async def save(
        self,
        registration_id: str,
        registration: Registration,
        /,
        uow: AsyncTransaction,
    ):
        data = {k: v for k, v in registration.items() if k not in ("id")}
        data["type"] = str(data["type"])
        document = self._collection.document(registration_id)
        uow.set(
            document,
            data,
            merge=True,
        )

from taiwan_geodoc_hub.modules.registration_managing.constants.registration_statuses import (
    RegistrationStatuses,
)

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
from taiwan_geodoc_hub.infrastructure.constants.collections import (
    Collections,
)
from taiwan_geodoc_hub.infrastructure.constants.types import (
    TenantId,
    SnapshotId,
)
from injector import inject


class RegistrationAdapter(RegistrationRepository[AsyncTransaction]):
    _collection: AsyncCollectionReference

    @inject
    def __init__(
        self, /, db: AsyncClient, tenant_id: TenantId, snapshot_id: SnapshotId
    ):
        self._collection = db.collection(
            str(Collections.registrations)
            .replace(":tenantId", tenant_id)
            .replace(":snapshotId", snapshot_id)
        )

    async def exists(self, registration_id: str, /, uow: AsyncTransaction):
        document = self._collection.document(registration_id)
        db: AsyncClient = uow._client
        document_snapshot = await anext(aiter(db.get_all([document], transaction=uow)))
        return document_snapshot.exists

    async def save(
        self,
        registration_id: str,
        data: Registration,
        /,
        uow: AsyncTransaction,
    ):
        registration: Registration = {k: v for k, v in data.items() if k not in ("id")}
        registration["type"] = str(registration["type"])
        registration["status"] = str(RegistrationStatuses.pending)
        document = self._collection.document(registration_id)
        uow.set(
            document,
            registration,
            merge=True,
        )

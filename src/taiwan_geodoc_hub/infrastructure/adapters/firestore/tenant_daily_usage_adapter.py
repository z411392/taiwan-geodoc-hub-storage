from google.cloud.firestore import (
    AsyncClient,
    AsyncCollectionReference,
    AsyncTransaction,
)
from taiwan_geodoc_hub.infrastructure.types.collection import (
    Collection,
)
from injector import inject
from taiwan_geodoc_hub.infrastructure.constants.tokens import TenantId
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.tenant_daily_usage_repository import (
    TenantDailyUsageRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.tenant_daily_usage import (
    TenantDailyUsage,
)
from datetime import datetime, timedelta, UTC


class TenantDailyUsageAdapter(TenantDailyUsageRepository[AsyncTransaction]):
    _collection: AsyncCollectionReference

    @inject
    def __init__(
        self,
        /,
        db: AsyncClient,
        tenant_id: TenantId,
    ):
        self._collection = db.collection(
            str(Collection.TenantDailyUsage).replace(":tenantId", tenant_id)
        )

    async def load(
        self,
        date: str,
        /,
        uow: AsyncTransaction,
    ):
        document = self._collection.document(date)
        db: AsyncClient = uow._client
        document_snapshot = await anext(aiter(db.get_all([document], transaction=uow)))
        if not document_snapshot.exists:
            return None
        return TenantDailyUsage(
            id=document_snapshot.id,
            **document_snapshot.to_dict(),
        )

    async def save(
        self,
        date: str,
        tenant_daily_usage: TenantDailyUsage,
        /,
        uow: AsyncTransaction,
    ):
        document = self._collection.document(date)
        data = {k: v for k, v in tenant_daily_usage.items() if k not in ("id")}
        if data.get("expiredAt") is None:
            expired_at = datetime.now(UTC) + timedelta(days=1)
            data.update(
                expiredAt=expired_at,
            )
        uow.set(
            document,
            data,
            merge=True,
        )

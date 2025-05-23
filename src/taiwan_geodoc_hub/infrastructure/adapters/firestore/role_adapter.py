from google.cloud.firestore import AsyncClient, AsyncCollectionReference, FieldFilter
from taiwan_geodoc_hub.infrastructure.constants.collections import Collections
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import (
    RoleDao,
)
from taiwan_geodoc_hub.infrastructure.constants.types import (
    TenantId,
)
from injector import inject
from taiwan_geodoc_hub.modules.access_managing.constants.roles import Roles
from taiwan_geodoc_hub.modules.access_managing.dtos.role import Role
from taiwan_geodoc_hub.modules.access_managing.constants.role_statuses import (
    RoleStatuses,
)
from typing import List
from google.cloud.firestore_v1.field_path import FieldPath


class RoleAdapter(RoleDao):
    _collection: AsyncCollectionReference

    @inject
    def __init__(self, /, db: AsyncClient, tenant_id: TenantId):
        self._collection = db.collection(
            str(Collections.roles).replace(":tenantId", tenant_id)
        )

    async def in_ids(self, *user_ids: List[str]) -> List[Role]:
        batch_size = 30
        roles: List[Role] = []
        for offset in range(0, len(user_ids), batch_size):
            documents = list(
                map(self._collection.document, user_ids[offset : offset + batch_size])
            )
            stream = (
                self._collection.where(
                    filter=FieldFilter(
                        FieldPath.document_id(),
                        "in",
                        documents,
                    )
                )
                # .select([])
                .stream()
            )
            async for document_snapshot in stream:
                role_data = document_snapshot.to_dict()
                role = Role(
                    id=document_snapshot.id,
                    type=Roles(role_data.get("type")),
                    status=RoleStatuses(role_data.get("status")),
                )
                roles.append(role)
        return roles

    async def by_id(self, user_id: str):
        roles = await self.in_ids(user_id)
        if len(roles) == 0:
            return None
        [role] = roles
        return role

from typing import TypedDict
from taiwan_geodoc_hub.modules.access_managing.types.tenant_status import (
    TenantStatus,
)


class Tenant(TypedDict):
    id: str
    name: str
    status: TenantStatus

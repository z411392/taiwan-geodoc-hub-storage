from typing import TypedDict
from taiwan_geodoc_hub.modules.access_managing.constants.tenant_statuses import (
    TenantStatuses,
)


class Tenant(TypedDict):
    id: str
    name: str
    status: TenantStatuses

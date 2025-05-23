from enum import Enum


class Collection(str, Enum):
    OCRResults = "ocrResults"
    Tenants = "tenants"
    Roles = "tenants/:tenantId/roles"
    Snapshots = "snapshots"
    Registrations = "snapshots/:snapshotId/registrations"
    TenantDailyUsage = "stats/usage/tenants/:tenantId/daily"
    SnapshotOwnerships = "snapshots/:snapshotId/ownerships"
    Processes = "processes"

    def __str__(self):
        return self.value

from enum import Enum


class Collections(str, Enum):
    ocrResults = "ocrResults"
    tenants = "tenants"
    roles = "tenants/:tenantId/roles"
    snapshots = "tenants/:tenantId/snapshots"
    registrations = "tenants/:tenantId/snapshots/:snapshotId/registrations"

    def __str__(self):
        return self.value

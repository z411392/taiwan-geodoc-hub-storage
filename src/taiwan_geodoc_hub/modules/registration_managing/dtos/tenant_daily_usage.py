from typing import TypedDict


class TenantDailyUsage(TypedDict):
    id: str
    snapshots: int

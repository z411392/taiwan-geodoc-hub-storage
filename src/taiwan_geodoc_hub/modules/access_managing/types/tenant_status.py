from enum import Enum


class TenantStatus(str, Enum):
    Pending = "pending"
    Approved = "approved"
    Rejected = "rejected"

    def __str__(self):
        return self.value

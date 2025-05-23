from enum import Enum


class RoleStatuses(str, Enum):
    Pending = "pending"
    Approved = "approved"
    Rejected = "rejected"

    def __str__(self):
        return self.value

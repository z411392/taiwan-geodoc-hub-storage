from enum import Enum


class RoleType(str, Enum):
    Manager = "manager"
    Member = "member"

    def __str__(self):
        return self.value

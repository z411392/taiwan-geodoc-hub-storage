from enum import Enum


class Roles(str, Enum):
    manager = "manager"
    member = "member"

    def __str__(self):
        return self.value

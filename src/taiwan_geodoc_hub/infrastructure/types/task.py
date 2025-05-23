from enum import Enum


class Task(str, Enum):
    ProjectingOwnerships = "projecting/ownerships"

    def __str__(self):
        return f"{self.value}"

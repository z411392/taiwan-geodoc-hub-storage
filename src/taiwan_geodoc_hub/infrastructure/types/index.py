from enum import Enum


class Index(str, Enum):
    Events = "events"
    Ownerships = "ownerships"

    def __str__(self):
        return f"{self.value}"

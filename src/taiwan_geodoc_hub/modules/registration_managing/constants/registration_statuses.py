from enum import Enum


class RegistrationStatuses(str, Enum):
    pending = "pending"
    completed = "completed"

    def __str__(self):
        return self.value

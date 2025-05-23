from enum import Enum


class RegistrationTypes(str, Enum):
    building = "building"
    land = "land"

    def __str__(self):
        return self.value

from enum import Enum


class RegistrationType(str, Enum):
    Building = "building"
    Land = "land"

    def __str__(self):
        return self.value

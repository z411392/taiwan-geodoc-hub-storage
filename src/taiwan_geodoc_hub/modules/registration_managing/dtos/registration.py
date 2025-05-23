from typing import TypedDict
from taiwan_geodoc_hub.modules.registration_managing.types.registration_type import (
    RegistrationType,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.土地登記 import (
    土地登記,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.建物登記 import (
    建物登記,
)
from typing import Union, Literal


class RegistrationBase(TypedDict):
    id: str
    text: str


class LandRegistration(RegistrationBase):
    type: Literal[RegistrationType.Land]
    json: 土地登記


class BuildingRegistration(RegistrationBase):
    type: Literal[RegistrationType.Building]
    json: 建物登記


Registration = Union[LandRegistration, BuildingRegistration]

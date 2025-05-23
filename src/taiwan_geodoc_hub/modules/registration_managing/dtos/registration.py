from typing import TypedDict
from taiwan_geodoc_hub.modules.registration_managing.constants.registration_types import (
    RegistrationTypes,
)
from taiwan_geodoc_hub.modules.registration_managing.constants.registration_statuses import (
    RegistrationStatuses,
)


class Registration(TypedDict):
    id: str
    type: RegistrationTypes
    text: str
    status: RegistrationStatuses
    userId: str

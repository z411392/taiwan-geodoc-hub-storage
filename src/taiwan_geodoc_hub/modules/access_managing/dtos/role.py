from typing import TypedDict
from taiwan_geodoc_hub.modules.access_managing.constants.roles import Roles


class Role(TypedDict):
    id: str
    type: Roles
    status: str

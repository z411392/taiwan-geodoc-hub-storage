from typing import TypedDict
from taiwan_geodoc_hub.modules.access_managing.types.role_type import RoleType


class Role(TypedDict):
    id: str
    type: RoleType
    status: str

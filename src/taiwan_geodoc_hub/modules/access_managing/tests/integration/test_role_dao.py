import pytest
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import (
    RoleDao,
)
from taiwan_geodoc_hub.infrastructure.constants.tokens import (
    TenantId,
)
from os import getenv
from taiwan_geodoc_hub.modules.access_managing.types.role_type import RoleType


# @pytest.mark.skip(reason="")
class TestRoleDao:
    @pytest.fixture(scope="module")
    def role_dao(self, injector: Injector):
        injector.binder.bind(TenantId, to=InstanceProvider(getenv("TENANT_ID")))
        role_dao = injector.get(RoleDao)
        return role_dao

    @pytest.mark.describe("要能夠取得 role")
    @pytest.mark.asyncio
    async def test_get_role_under_tenant(self, role_dao: RoleDao):
        user_id = getenv("USER_ID")
        role = await role_dao.by_id(user_id=user_id)
        assert role.get("type") == RoleType.Manager

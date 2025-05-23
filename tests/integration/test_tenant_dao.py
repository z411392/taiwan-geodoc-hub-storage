import pytest
from injector import Injector
from taiwan_geodoc_hub.modules.access_managing.domain.ports.tenant_dao import (
    TenantDao,
)
from os import getenv


# @pytest.mark.skip(reason="")
class TestTenantDao:
    @pytest.fixture(scope="module")
    def tenant_dao(self, injector: Injector):
        tenant_dao = injector.get(TenantDao)
        return tenant_dao

    @pytest.mark.describe("要能夠取得 tenant")
    @pytest.mark.asyncio
    async def test_get_tenant_by_id(self, tenant_dao: TenantDao):
        tenant_id: str = getenv("TENANT_ID")
        tenant = await tenant_dao.by_id(tenant_id)
        if tenant is None:
            return pytest.fail(f"無法取得 tenant, tenant_id={tenant_id}")
        assert tenant.get("id") == tenant_id

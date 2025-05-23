import pytest
from httpx import AsyncClient


# @pytest.mark.skip(reason="")
class TestSystemMaintaining:
    @pytest.mark.describe("要能夠檢查系統是否正常運作")
    @pytest.mark.asyncio
    async def test_checking_health(self, client: AsyncClient):
        response = await client.get("/__/health")
        assert response.status_code == 200

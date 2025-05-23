import pytest
from httpx import AsyncClient
from os import getenv
from json import dumps


# @pytest.mark.skip(reason="")
class TestRegistrationManaging:
    @pytest.mark.describe("要能夠上傳謄本並解析 PDF 中的文字")
    @pytest.mark.asyncio
    async def test_uploading_pdf(
        self,
        client: AsyncClient,
        sample_pdf: str,
    ):
        response = await client.post(
            f"/tenants/{getenv('TENANT_ID')}/pdf",
            content=dumps(
                dict(
                    name="建物謄本.pdf",
                    content=sample_pdf,
                ),
                ensure_ascii=False,
            ).encode("utf-8"),
            headers=dict(Authorization=f"bearer {getenv('ID_TOKEN')}"),
        )
        assert response.status_code == 200

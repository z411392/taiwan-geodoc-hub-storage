import pytest
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.infrastructure.utils.hashers.bytes_hasher import (
    BytesHasher,
)
from taiwan_geodoc_hub.infrastructure.constants.tokens import (
    UserId,
    TenantId,
    SnapshotId,
)
from taiwan_geodoc_hub.modules.registration_managing.application.commands.upload_pdf import (
    UploadPDF,
)
from base64 import b64decode
from os import getenv


# @pytest.mark.skip(reason="")
class TestBytesHasher:
    @pytest.fixture
    def hash_bytes(self, injector: Injector):
        return injector.get(BytesHasher)

    @pytest.mark.describe("要能夠上傳 pdf")
    @pytest.mark.asyncio
    async def test_upload_pdf(
        self,
        hash_bytes: BytesHasher,
        injector: Injector,
        sample_pdf: str,
    ):
        pdf = b64decode(sample_pdf)
        snapshot_id = hash_bytes(pdf)
        injector.binder.bind(UserId, to=InstanceProvider(getenv("USER_ID")))
        injector.binder.bind(TenantId, to=InstanceProvider(getenv("TENANT_ID")))
        injector.binder.bind(SnapshotId, to=InstanceProvider(snapshot_id))
        handler = injector.get(UploadPDF)
        await handler("建物謄本.pdf", pdf)

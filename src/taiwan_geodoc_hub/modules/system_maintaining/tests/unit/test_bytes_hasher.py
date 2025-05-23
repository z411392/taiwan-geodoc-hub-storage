import pytest
from taiwan_geodoc_hub.infrastructure.utils.hashers.bytes_hasher import (
    BytesHasher,
)
from injector import Injector


# @pytest.mark.skip(reason="")
class TestBytesHasher:
    @pytest.fixture
    def hash_bytes(self, injector: Injector):
        return injector.get(BytesHasher)

    @pytest.mark.describe("要能夠產生 bytes 的 uuid")
    def test_bytes_uuid(
        self,
        hash_bytes: BytesHasher,
        sample_image: bytes,
        sample_image_hash: str,
    ):
        hash_calculated = hash_bytes(sample_image)
        assert hash_calculated == sample_image_hash

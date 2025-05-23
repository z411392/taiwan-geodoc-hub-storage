import pytest
from injector import Injector
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.cached_ocr_processor import (
    CachedOCRProcessor,
)


# @pytest.mark.skip(reason="")
class TestOCRSpace:
    @pytest.fixture(scope="module")
    def ocr_service(self, injector: Injector):
        return injector.get(CachedOCRProcessor)

    @pytest.mark.describe("要能夠 ocr")
    @pytest.mark.asyncio
    async def test_ocr(
        self,
        sample_image: bytes,
        ocr_service: CachedOCRProcessor,
        sample_ocr_result: str,
    ):
        text = await ocr_service(sample_image)
        assert text == sample_ocr_result

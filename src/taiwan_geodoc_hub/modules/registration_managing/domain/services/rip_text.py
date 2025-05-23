from taiwan_geodoc_hub.infrastructure.utils.helpers.documents.pdf_text_ripper import (
    PDFTextRipper,
)
from io import StringIO
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.cached_ocr_processor import (
    CachedOCRProcessor,
)
from injector import inject


class RipText:
    _ocr_processor: CachedOCRProcessor

    @inject
    def __init__(
        self,
        /,
        ocr_processor: CachedOCRProcessor,
    ):
        self._ocr_processor = ocr_processor

    async def __call__(self, pdf: bytes):
        pdf_text_ripper = PDFTextRipper(pdf)
        string = StringIO()
        for is_image, content in pdf_text_ripper:
            if is_image:
                ocr_result = await self._ocr_processor(content)
                string.write(f"\n{ocr_result}")
            else:
                string.write(f"\n{content}")
        text = string.getvalue().strip()
        return text

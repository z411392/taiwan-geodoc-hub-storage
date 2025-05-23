from taiwan_geodoc_hub.modules.registration_managing.domain.ports.cached_ocr_processor import (
    CachedOCRProcessor,
)
from injector import inject
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_processor import (
    OCRProcessor,
)
from google.cloud.firestore import AsyncClient, async_transactional, AsyncTransaction
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_result_repository import (
    OCRResultRepository,
)
from taiwan_geodoc_hub.infrastructure.utils.hashers.bytes_hasher import (
    BytesHasher,
)


class PerformOCR(CachedOCRProcessor):
    _ocr_processor: OCRProcessor
    _db: AsyncClient
    _ocr_result_repository: OCRResultRepository
    _hash_bytes: BytesHasher

    @inject
    def __init__(
        self,
        /,
        ocr_processor: OCRProcessor,
        db: AsyncClient,
        ocr_result_repository: OCRResultRepository,
        bytes_hasher: BytesHasher,
    ):
        self._ocr_processor = ocr_processor
        self._db = db
        self._ocr_result_repository = ocr_result_repository
        self._hash_bytes = bytes_hasher

    async def __call__(self, image: bytes, language: str = "cht"):
        ocr_result_id = self._hash_bytes(image)

        @async_transactional
        async def run_in_transaction(transaction: AsyncTransaction):
            ocr_result = await self._ocr_result_repository.load(
                ocr_result_id,
                uow=transaction,
            )
            if ocr_result is not None:
                return ocr_result
            ocr_result = await self._ocr_processor(image, language)
            await self._ocr_result_repository.save(
                ocr_result_id,
                ocr_result,
                uow=transaction,
            )
            return ocr_result

        ocr_result = await run_in_transaction(self._db.transaction())
        return ocr_result

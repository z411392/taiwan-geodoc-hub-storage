from google.cloud.firestore import (
    AsyncClient,
    AsyncCollectionReference,
    AsyncTransaction,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.ocr_result import (
    OCRResult,
)
from taiwan_geodoc_hub.infrastructure.constants.collections import (
    Collections,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_result_repository import (
    OCRResultRepository,
)
from injector import inject


class OCRResultAdapter(OCRResultRepository[AsyncTransaction]):
    _collection: AsyncCollectionReference

    @inject
    def __init__(self, /, db: AsyncClient):
        self._collection = db.collection(str(Collections.ocrResults))

    async def save(self, ocr_result_id: str, text: str, /, uow: AsyncTransaction):
        document = self._collection.document(ocr_result_id)
        ocr_result = OCRResult(text=text)
        uow.set(document, ocr_result, merge=True)

    async def load(self, ocr_result_id: str, /, uow: AsyncTransaction):
        document = self._collection.document(ocr_result_id)
        db: AsyncClient = uow._client
        document_snapshot = await anext(aiter(db.get_all([document], transaction=uow)))
        if not document_snapshot.exists:
            return None
        ocr_result: OCRResult = document_snapshot.to_dict()
        return ocr_result.get("text")

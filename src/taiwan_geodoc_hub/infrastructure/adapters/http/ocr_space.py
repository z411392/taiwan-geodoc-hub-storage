from base64 import b64encode
from injector import inject
from aiohttp import ClientSession
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_processor import (
    OCRProcessor,
)


class OCRSpace(OCRProcessor):
    _endpoint: str = "https://api.ocr.space/parse/image"
    _api_key: str

    @inject
    def __init__(self, /, api_key: str):
        self._api_key = api_key

    async def __call__(self, image: bytes, language: str = "cht") -> str:
        base64_encoded = b64encode(image).decode("utf-8")
        base64_image = f"data:image/jpeg;base64,{base64_encoded}"
        body = {
            "apikey": self._api_key,
            "language": language,
            "base64Image": base64_image,
        }
        async with ClientSession() as session:
            async with session.post(self._endpoint, data=body) as response:
                payload: dict = await response.json()
                if "ParsedResults" not in payload:
                    return ""
                results: dict = payload["ParsedResults"]
                joined = "".join(result["ParsedText"] for result in results)
                trimmed = joined.replace("\r", "").replace("\n", "").strip()
                return trimmed

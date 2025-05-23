from injector import inject
from os import getenv
from taiwan_geodoc_hub.infrastructure.types.index import Index
from typing import TypedDict, List, Generic, TypeVar
from httpx import AsyncClient as HttpConnectionPool


class SearchRequestBody(TypedDict, total=False):
    q: str
    offset: int
    hitsPerPage: int
    filter: List[str]
    attributesToSearchOn: List[str]
    attributesToRetrieve: List[str]
    sort: List[str]


T = TypeVar("T")


class SearchResponseBody(TypedDict, Generic[T]):
    hits: List[T]
    query: str
    processingTimeMs: int
    limit: int
    offset: int
    estimatedTotalHits: int


class SetupIndexRequestBody(TypedDict, total=False):
    searchableAttributes: List[str]
    filterableAttributes: List[str]
    sortableAttributes: List[str]


class SetupIndexResponseBody(TypedDict):
    taskUid: int
    indexUid: str
    status: str
    type: str
    enqueuedAt: str


class Meilisearch:
    _api_key: str
    _endpoint: str
    _http_connection_pool: HttpConnectionPool

    @inject
    def __init__(
        self,
        http_connection_pool: HttpConnectionPool,
    ):
        self._api_key = getenv("MEILISEARCH_API_KEY")
        self._endpoint = getenv("MEILISEARCH_ENDPOINT")
        self._http_connection_pool = http_connection_pool

    async def save(self, index: Index, document: dict):
        url = f"{self._endpoint}/indexes/{index}/documents"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        response = await self._http_connection_pool.post(
            url, json=document, headers=headers
        )
        if response.status_code != 200:
            return None
        return response.json()

    async def search(
        self,
        index: Index,
        payload: SearchRequestBody,
    ):
        url = f"{self._endpoint}/indexes/{index}/search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        response = await self._http_connection_pool.post(
            url, json=payload, headers=headers
        )
        if response.status_code != 200:
            return None
        try:
            body: SearchResponseBody = response.json()
            return body
        except Exception:
            return None

    async def setup_index(self, index: Index, settings: SetupIndexRequestBody):
        url = f"{self._endpoint}/indexes/{index}/settings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        response = await self._http_connection_pool.patch(
            url, json=settings, headers=headers
        )
        if response.status_code != 200:
            return None
        try:
            body: SetupIndexResponseBody = response.json()
            return body
        except Exception:
            return None

from taiwan_geodoc_hub.modules.access_managing.dtos.credentials import (
    Credentials,
)
from typing import Optional
from os import getenv
from httpx import AsyncClient as HttpConnectionPool
from injector import inject


class GoogleSecureTokenApi:
    _endpoint: str = "https://securetoken.googleapis.com/v1"
    _api_key: str
    _http_connection_pool: HttpConnectionPool

    @inject
    def __init__(self, /, http_connection_pool: HttpConnectionPool):
        self._api_key = getenv("API_KEY")
        self._http_connection_pool = http_connection_pool

    async def refresh_token(self, refresh_token: str) -> Optional[Credentials]:
        url = f"{self._endpoint}/token?key={self._api_key}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = dict(grant_type="refresh_token", refresh_token=refresh_token)
        response = await self._http_connection_pool.post(
            url, headers=headers, data=body
        )
        if response.status_code != 200:
            return None
        data: dict = response.json()
        return Credentials(
            idToken=data["id_token"],
            refreshToken=data["refresh_token"],
        )

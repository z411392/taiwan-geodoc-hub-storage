from taiwan_geodoc_hub.modules.access_managing.domain.ports.token_service import (
    TokenService,
)
from taiwan_geodoc_hub.modules.access_managing.dtos.credentials import (
    Credentials,
)
from typing import Optional
import jwt
from time import time
from os import getenv
from aiohttp import ClientSession


class TokenAdapter(TokenService):
    def __init__(self):
        self.api_key = getenv("API_KEY")

    async def refresh_token(self, refresh_token: str) -> Optional[Credentials]:
        url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = dict(grant_type="refresh_token", refresh_token=refresh_token)
        async with ClientSession() as session:
            async with session.post(url, headers=headers, data=body) as response:
                if response.status != 200:
                    return None
                data: dict = await response.json()
                return Credentials(
                    idToken=data["id_token"],
                    refreshToken=data["refresh_token"],
                )

    def is_token_valid(self, id_token: str) -> bool:
        try:
            decoded = jwt.decode(id_token, options=dict(verify_signature=False))
            now = int(time())
            return "exp" in decoded and decoded["exp"] > now + 600
        except Exception:
            return False

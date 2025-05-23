from typing import TypedDict


class Credentials(TypedDict):
    idToken: str
    refreshToken: str

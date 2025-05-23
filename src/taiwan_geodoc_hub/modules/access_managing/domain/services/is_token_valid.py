from jwt import decode
from time import time


def is_token_valid(id_token: str):
    try:
        decoded = decode(id_token, options={"verify_signature": False})
        now = int(time())
        return "exp" in decoded and decoded["exp"] > now + 600
    except Exception:
        return False

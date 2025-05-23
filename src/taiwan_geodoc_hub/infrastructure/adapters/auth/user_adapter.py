from firebase_admin.auth import (
    UserRecord,
    get_users,
    UidIdentifier,
    GetUsersResult,
)
from typing import Optional, List
from firebase_admin.auth import verify_id_token
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import (
    UserDao,
)
from asyncio import get_running_loop


class UserAdapter(UserDao):
    def _in_ids(self, *user_ids: List[str]):
        identifiers = list(map(UidIdentifier, user_ids))
        batch_size = 100
        users: List[UserRecord] = []
        for offset in range(0, len(identifiers), batch_size):
            batch = list(map(UidIdentifier, user_ids[offset : offset + batch_size]))
            try:
                result: GetUsersResult = get_users(identifiers=batch)
                users.extend(result.users)
            except Exception:
                pass
        return users

    def _by_id(self, user_id: str):
        users: List[UserRecord] = self._in_ids(user_id)
        if len(users) == 0:
            return None
        [user] = users
        return user

    async def in_ids(self, *user_ids: List[str]):
        return await get_running_loop().run_in_executor(None, self._in_ids, *user_ids)

    async def by_id(self, user_id: str):
        return await get_running_loop().run_in_executor(None, self._by_id, user_id)

    def _from_id_token(self, id_token: str):
        try:
            decoded_claims: Optional[dict] = verify_id_token(id_token)
            if decoded_claims is None:
                return None
            user_id: Optional[str] = decoded_claims.get("uid")
            if user_id is None:
                return None
            user: Optional[UserRecord] = self._by_id(user_id)
            return user
        except Exception:
            return None

    async def from_id_token(self, id_token: str):
        return await get_running_loop().run_in_executor(
            None, self._from_id_token, id_token
        )

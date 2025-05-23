from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import (
    UserDao,
)
from logging import Logger
from time import perf_counter


class ResolveUser:
    _user_dao: UserDao
    _logger: Logger

    @inject
    def __init__(self, user_dao: UserDao, logger: Logger):
        self._user_dao = user_dao
        self._logger = logger

    async def __call__(self, id_token: str):
        start = perf_counter()
        try:
            user = await self._user_dao.from_id_token(id_token)
            self._logger.info(
                "ResolveUser finished", extra=dict(elapsed=perf_counter() - start)
            )
            return user
        except Exception:
            self._logger.exception(
                "ResolveUser failed",
            )
            raise

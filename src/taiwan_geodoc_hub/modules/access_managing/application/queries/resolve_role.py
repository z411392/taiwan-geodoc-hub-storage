from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import (
    RoleDao,
)
from logging import Logger
from time import perf_counter
from taiwan_geodoc_hub.modules.access_managing.constants.role_statuses import (
    RoleStatuses,
)


class ResolveRole:
    _role_dao: RoleDao
    _logger: Logger

    @inject
    def __init__(
        self,
        role_dao: RoleDao,
        logger: Logger,
    ):
        self._role_dao = role_dao
        self._logger = logger

    async def __call__(self, user_id: str):
        start = perf_counter()
        try:
            role = await self._role_dao.by_id(user_id=user_id)
            if role and role.get("status") != RoleStatuses.Approved:
                role = None
            self._logger.info(
                "ResolveRole finished", extra=dict(elapsed=perf_counter() - start)
            )
            return role
        except Exception:
            self._logger.exception(
                "ResolveRole failed",
            )
            raise

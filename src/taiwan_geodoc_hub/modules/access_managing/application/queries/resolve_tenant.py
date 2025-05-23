from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.tenant_dao import (
    TenantDao,
)
from logging import Logger
from time import perf_counter
from taiwan_geodoc_hub.modules.access_managing.types.tenant_status import (
    TenantStatus,
)


class ResolveTenant:
    _tenant_dao: TenantDao
    _logger: Logger

    @inject
    def __init__(
        self,
        tenant_dao: TenantDao,
        logger: Logger,
    ):
        self._tenant_dao = tenant_dao
        self._logger = logger

    async def __call__(self, tenant_id: str):
        start = perf_counter()
        try:
            tenant = await self._tenant_dao.by_id(tenant_id)
            if tenant and tenant.get("status") != TenantStatus.Approved:
                tenant = None
            self._logger.info(
                "ResolveTenant finished", extra=dict(elapsed=perf_counter() - start)
            )
            return tenant
        except Exception:
            self._logger.exception(
                "ResolveTenant failed",
            )
            raise

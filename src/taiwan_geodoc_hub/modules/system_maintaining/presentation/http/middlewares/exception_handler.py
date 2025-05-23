from starlette.requests import Request
from starlette.responses import JSONResponse
from taiwan_geodoc_hub.modules.access_managing.exceptions.unauthorized import (
    Unauthorized,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.tenant_not_found import (
    TenantNotFound,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.permission_denied import (
    PermissionDenied,
)
from taiwan_geodoc_hub.modules.registration_managing.exceptions.tenant_max_snapshots_daily_limit_reached import (
    TenantMaxSnapshotsDailyLimitReached,
)


class ExceptionHandler:
    async def __call__(self, request: Request, exception: Exception):
        if isinstance(exception, Unauthorized):
            return JSONResponse(
                dict(
                    success=False,
                    data=dict(exception),
                ),
                status_code=401,
            )
        if isinstance(exception, TenantNotFound):
            return JSONResponse(
                dict(
                    success=False,
                    data=dict(exception),
                ),
                status_code=404,
            )
        if isinstance(exception, PermissionDenied):
            return JSONResponse(
                dict(
                    success=False,
                    data=dict(exception),
                ),
                status_code=403,
            )
        if isinstance(exception, TenantMaxSnapshotsDailyLimitReached):
            return JSONResponse(
                dict(
                    success=False,
                    data=dict(exception),
                ),
                status_code=403,
            )
        return JSONResponse(
            dict(
                success=False,
                data=dict(exception=str(exception)),
            ),
            status_code=500,
        )


exception_handler = ExceptionHandler()

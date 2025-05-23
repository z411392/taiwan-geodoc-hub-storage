from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from injector import InstanceProvider
from taiwan_geodoc_hub.modules.access_managing.application.queries.resolve_tenant import (
    ResolveTenant,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.tenant_not_found import (
    TenantNotFound,
)
from typing import Callable, Coroutine
from taiwan_geodoc_hub.infrastructure.constants.tokens import TenantId
from taiwan_geodoc_hub.infrastructure.lifespan import ensure_injector


def with_resolving_tenant(enforce: bool):
    class Middleware(BaseHTTPMiddleware):
        async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Coroutine[None, None, Response]],
        ):
            injector = await ensure_injector(request)
            tenant_id = request.path_params.get("tenant_id")
            handler = injector.get(ResolveTenant)
            tenant = await handler(tenant_id)
            if tenant is None and enforce:
                raise TenantNotFound(tenant_id)
            if tenant:
                request.scope["tenant"] = tenant
                injector.binder.bind(TenantId, to=InstanceProvider(tenant.get("id")))
            return await call_next(request)

    return Middleware

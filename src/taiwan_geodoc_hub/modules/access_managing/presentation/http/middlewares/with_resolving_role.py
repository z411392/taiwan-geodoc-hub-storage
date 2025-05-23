from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from injector import InstanceProvider
from taiwan_geodoc_hub.modules.access_managing.application.queries.resolve_role import (
    ResolveRole,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.permission_denied import (
    PermissionDenied,
)
from taiwan_geodoc_hub.modules.access_managing.types.role_type import RoleType
from typing import Optional, Callable, Coroutine
from firebase_admin.auth import UserRecord
from taiwan_geodoc_hub.modules.access_managing.domain.services.is_root import (
    is_root,
)
from taiwan_geodoc_hub.modules.access_managing.dtos.role import Role
from taiwan_geodoc_hub.modules.access_managing.types.role_status import (
    RoleStatus,
)
from taiwan_geodoc_hub.infrastructure.lifespan import ensure_injector


def with_resolving_role(enforce: bool):
    class Middleware(BaseHTTPMiddleware):
        async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Coroutine[None, None, Response]],
        ):
            injector = await ensure_injector(request)
            user: UserRecord = request.scope["user"]
            role: Optional[Role] = None
            if is_root(user.uid):
                role = Role(
                    id=user.uid,
                    name=RoleType.Manager,
                    status=RoleStatus.Approved,
                )
            else:
                handler = injector.get(ResolveRole)
                role = await handler(user.uid)
            if role is None and enforce is True:
                raise PermissionDenied()
            if role:
                request.scope["role"] = role
                injector.binder.bind(RoleType, to=InstanceProvider(role.get("type")))
            return await call_next(request)

    return Middleware

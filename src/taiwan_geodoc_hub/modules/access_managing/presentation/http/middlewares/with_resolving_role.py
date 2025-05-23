from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.modules.access_managing.application.queries.resolve_role import (
    ResolveRole,
)
from taiwan_geodoc_hub.modules.access_managing.exceptions.permission_denied import (
    PermissionDenied,
)
from taiwan_geodoc_hub.modules.access_managing.constants.roles import Roles
from typing import Optional, Callable, Coroutine
from firebase_admin.auth import UserRecord
from taiwan_geodoc_hub.modules.access_managing.domain.services.is_root import (
    is_root,
)
from taiwan_geodoc_hub.infrastructure.constants.types import Role as RoleToken
from taiwan_geodoc_hub.modules.access_managing.dtos.role import Role
from taiwan_geodoc_hub.modules.access_managing.constants.role_statuses import (
    RoleStatuses,
)


def with_resolving_role(enforce: bool):
    class Middleware(BaseHTTPMiddleware):
        async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Coroutine[None, None, Response]],
        ):
            injector: Injector = request.scope["injector"]
            user: UserRecord = request.scope["user"]
            role: Optional[Role] = None
            if is_root(user.uid):
                role = Role(
                    id=user.uid,
                    name=Roles.manager,
                    status=RoleStatuses.Approved,
                )
            else:
                handler = injector.get(ResolveRole)
                role = await handler(user.uid)
            if role is None and enforce is True:
                raise PermissionDenied()
            if role:
                request.scope["role"] = role
                injector.binder.bind(RoleToken, to=InstanceProvider(role))
            return await call_next(request)

    return Middleware

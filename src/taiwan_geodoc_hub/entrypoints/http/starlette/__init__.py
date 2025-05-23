from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from taiwan_geodoc_hub.infrastructure.lifespan import lifespan
from taiwan_geodoc_hub.modules.system_maintaining.presentation.http.middlewares.with_resolving_trace_id import (
    WithResolvingTraceId,
)
from taiwan_geodoc_hub.modules.system_maintaining.presentation.http.middlewares.exception_handler import (
    exception_handler,
)
from taiwan_geodoc_hub.modules.registration_managing.presentation.http.controllers.on_uploading_pdf import (
    on_uploading_pdf,
)
from taiwan_geodoc_hub.modules.access_managing.presentation.http.middlewares.with_resolving_user import (
    with_resolving_user,
)
from taiwan_geodoc_hub.modules.access_managing.presentation.http.middlewares.with_resolving_tenant import (
    with_resolving_tenant,
)
from taiwan_geodoc_hub.modules.access_managing.presentation.http.middlewares.with_resolving_role import (
    with_resolving_role,
)


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(
        WithResolvingTraceId,
    ),
    Middleware(
        ExceptionMiddleware,
        handlers={Exception: exception_handler},
    ),
]

routes = [
    Route(
        "/tenants/{tenant_id}/pdf",
        on_uploading_pdf,
        methods=["POST"],
        middleware=[
            Middleware(
                with_resolving_user(enforce=True),
            ),
            Middleware(
                with_resolving_tenant(enforce=True),
            ),
            Middleware(
                with_resolving_role(enforce=True),
            ),
        ],
    ),
]

app = Starlette(
    middleware=middleware,
    lifespan=lifespan,
    routes=routes,
    debug=False,
)

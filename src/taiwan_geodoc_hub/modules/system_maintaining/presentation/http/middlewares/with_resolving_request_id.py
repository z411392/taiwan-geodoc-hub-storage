from starlette.middleware.base import BaseHTTPMiddleware
from injector import Injector, InstanceProvider
from taiwan_geodoc_hub.infrastructure.constants.types import RequestId
from taiwan_geodoc_hub.infrastructure.utils.generators.request_id_generator import (
    RequestIdGenerator,
)


class WithResolvingRequestId(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        injector: Injector = request.scope["injector"]
        next_request_id = injector.get(RequestIdGenerator)
        request_id = next_request_id()
        request.scope["request_id"] = request_id
        injector.binder.bind(RequestId, to=InstanceProvider(request_id))
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        return response

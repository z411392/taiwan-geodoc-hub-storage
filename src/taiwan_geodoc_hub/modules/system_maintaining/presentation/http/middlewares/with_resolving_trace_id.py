from starlette.middleware.base import BaseHTTPMiddleware
from injector import InstanceProvider
from taiwan_geodoc_hub.infrastructure.constants.tokens import TraceId
from taiwan_geodoc_hub.infrastructure.utils.generators.trace_id_generator import (
    TraceIdGenerator,
)
from taiwan_geodoc_hub.infrastructure.lifespan import ensure_injector


class WithResolvingTraceId(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        injector = await ensure_injector(request)
        next_trace_id = injector.get(TraceIdGenerator)
        trace_id = next_trace_id()
        request.scope["trace_id"] = trace_id
        injector.binder.bind(TraceId, to=InstanceProvider(trace_id))
        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        return response

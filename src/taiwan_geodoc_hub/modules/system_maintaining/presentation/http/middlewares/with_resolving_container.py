from starlette.middleware.base import BaseHTTPMiddleware
from injector import Injector


class WithResolvingContainer(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        parent: Injector = request.app.state.injector
        injector = parent.create_child_injector()
        request.scope["injector"] = injector
        return await call_next(request)

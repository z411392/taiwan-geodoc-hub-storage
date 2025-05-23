from operator import itemgetter
from taiwan_geodoc_hub.modules.access_managing.application.queries.resolve_credentials import (
    ResolveCredentials,
)
from taiwan_geodoc_hub.infrastructure.utils.generators.trace_id_generator import (
    TraceIdGenerator,
)
from injector import InstanceProvider
from taiwan_geodoc_hub.infrastructure.constants.tokens import TraceId
from click.core import Context
from taiwan_geodoc_hub.infrastructure.lifespan import ensure_injector


async def login(context: Context):
    injector = await ensure_injector(context)
    next_trace_id = injector.get(TraceIdGenerator)
    trace_id = next_trace_id()
    injector.binder.bind(TraceId, to=InstanceProvider(trace_id))
    handler = injector.get(ResolveCredentials)
    credentials = await handler()
    id_token = itemgetter("idToken")(credentials)
    print(id_token)

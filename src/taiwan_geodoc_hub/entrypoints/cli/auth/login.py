from operator import itemgetter
from taiwan_geodoc_hub.infrastructure.lifespan import lifespan
from taiwan_geodoc_hub.modules.access_managing.application.queries.resolve_credentials import (
    ResolveCredentials,
)
from taiwan_geodoc_hub.infrastructure.utils.generators.request_id_generator import (
    RequestIdGenerator,
)
from injector import InstanceProvider
from taiwan_geodoc_hub.infrastructure.constants.types import RequestId
from taiwan_geodoc_hub.entrypoints.cli.auth.app import app


@app.async_command()
async def login():
    async with lifespan() as injector:
        try:
            next_request_id = injector.get(RequestIdGenerator)
            request_id = next_request_id()
            injector.binder.bind(RequestId, to=InstanceProvider(request_id))
            handler = injector.get(ResolveCredentials)
            credentials = await handler()
            id_token = itemgetter("idToken")(credentials)
            print(id_token)
        except Exception as exception:
            print(str(exception))

from typing import Optional, Union
from contextlib import asynccontextmanager
from starlette.applications import Starlette
from starlette.requests import Request
from injector import Injector
from google.cloud.pubsub import PublisherClient
from time import tzset
from taiwan_geodoc_hub.infrastructure.utils.firebase.boot_firebase import (
    boot_firebase,
)
from taiwan_geodoc_hub.infrastructure.utils.firebase.ensure_topics import ensure_topics
from taiwan_geodoc_hub.infrastructure.utils.firebase.dispose_firebase import (
    dispose_firebase,
)
from taiwan_geodoc_hub.infrastructure.utils.logging.setup_logging import setup_logging
from taiwan_geodoc_hub.modules.access_managing.access_managing_module import (
    AccessManagingModule,
)
from taiwan_geodoc_hub.modules.registration_managing.registration_managing_module import (
    RegistrationManagingModule,
)
from taiwan_geodoc_hub.modules.system_maintaining.system_maintaining_module import (
    SystemMaintainingModule,
)
from click.core import Context
from httpx import AsyncClient as HttpConnectionPool
from taiwan_geodoc_hub.infrastructure.utils.environments import is_cli

injector: Optional[Injector] = None


async def startup():
    global injector
    tzset()
    boot_firebase()
    setup_logging()
    injector = Injector(
        [
            AccessManagingModule(),
            RegistrationManagingModule(),
            SystemMaintainingModule(),
        ]
    )
    if not is_cli():
        await ensure_topics(injector.get(PublisherClient))
    return injector


async def shutdown():
    global injector
    try:
        httpx = injector.get(HttpConnectionPool)
        if httpx:
            await httpx.aclose()
    except Exception:
        pass
    dispose_firebase()
    injector = None


async def ensure_injector(context: Optional[Union[Request, Context]] = None):
    if context is None:
        return await startup()

    if isinstance(context, Request):
        if "injector" not in context.scope:
            context.scope["injector"] = (
                context.app.state.injector.create_child_injector()
            )
        return context.scope["injector"]

    if isinstance(context, Context):
        return context.obj


@asynccontextmanager
async def lifespan(app=None):
    injector = await startup()
    if app:
        if isinstance(app, Starlette):
            app.state.injector = injector
        yield
    else:
        yield injector
    await shutdown()

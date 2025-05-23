from injector import Module, InstanceProvider, ClassProvider, Provider
from google.cloud.firestore import AsyncClient
from firebase_admin.firestore_async import client
from taiwan_geodoc_hub.infrastructure.adapters.pubsub.event_publisher import (
    EventPublisher,
)
from google.cloud.pubsub import PublisherClient
from taiwan_geodoc_hub.modules.system_maintaining.domain.ports.process_manager_repository import (
    ProcessManagerRepository,
)
from taiwan_geodoc_hub.infrastructure.adapters.firestore.process_manager_adapter import (
    ProcessManagerAdapter,
)
from taiwan_geodoc_hub.infrastructure.utils.hashers.bytes_hasher import BytesHasher
from taiwan_geodoc_hub.infrastructure.utils.generators.trace_id_generator import (
    TraceIdGenerator,
)
from typing import Optional
from logging import Logger, LoggerAdapter, getLogger
from taiwan_geodoc_hub.infrastructure.constants.tokens import (
    TraceId,
    UserId,
    TenantId,
)
from httpx import AsyncClient as HttpConnectionPool


class LoggerProvider(Provider[Logger]):
    def get(self, injector):
        trace_id: Optional[str] = None
        user_id: Optional[str] = None
        tenant_id: Optional[str] = None
        try:
            trace_id = injector.get(TraceId)
            user_id = injector.get(UserId)
            tenant_id = injector.get(TenantId)
        except Exception:
            pass
        logger = LoggerAdapter(
            getLogger(trace_id),
            dict(
                userId=user_id,
                tenantId=tenant_id,
            ),
        )
        return logger


class SystemMaintainingModule(Module):
    def configure(self, binder):
        binder.bind(
            Logger,
            to=LoggerProvider(),
        )
        binder.bind(AsyncClient, to=InstanceProvider(client()))
        pubsub = PublisherClient()
        binder.bind(PublisherClient, to=InstanceProvider(pubsub))
        binder.bind(EventPublisher, to=ClassProvider(EventPublisher))
        binder.bind(
            ProcessManagerRepository,
            to=ClassProvider(ProcessManagerAdapter),
        )
        binder.bind(TraceIdGenerator, to=ClassProvider(TraceIdGenerator))
        binder.bind(BytesHasher, to=ClassProvider(BytesHasher))
        binder.bind(HttpConnectionPool, to=InstanceProvider(HttpConnectionPool()))

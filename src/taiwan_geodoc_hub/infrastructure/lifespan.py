from starlette.applications import Starlette
from typing import Optional
from contextlib import asynccontextmanager
from injector import Injector, InstanceProvider, ClassProvider
from os import getenv
from firebase_admin import initialize_app, get_app, delete_app
from firebase_admin.credentials import Certificate
from re import sub
from google.cloud.firestore import AsyncClient
from firebase_admin.firestore_async import client
from logging import basicConfig, INFO, WARNING, getLogger, StreamHandler
from taiwan_geodoc_hub.infrastructure.utils.logging.cloud_logging_json_formatter import (
    CloudLoggingJSONFormatter,
)
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import (
    UserDao,
)
from taiwan_geodoc_hub.infrastructure.adapters.auth.user_adapter import UserAdapter
from taiwan_geodoc_hub.modules.access_managing.domain.ports.tenant_dao import (
    TenantDao,
)
from taiwan_geodoc_hub.infrastructure.adapters.firestore.tenant_adapter import (
    TenantAdapter,
)
from taiwan_geodoc_hub.infrastructure.adapters.firestore.ocr_result_adapter import (
    OCRResultAdapter,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_result_repository import (
    OCRResultRepository,
)
from taiwan_geodoc_hub.infrastructure.adapters.firestore.registration_adapter import (
    RegistrationAdapter,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.registration_repository import (
    RegistrationRepository,
)
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import (
    RoleDao,
)
from taiwan_geodoc_hub.infrastructure.adapters.firestore.role_adapter import RoleAdapter
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_processor import (
    OCRProcessor,
)
from taiwan_geodoc_hub.infrastructure.adapters.http.ocr_space import OCRSpace
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.cached_ocr_processor import (
    CachedOCRProcessor,
)
from taiwan_geodoc_hub.modules.registration_managing.application.queries.perform_ocr import (
    PerformOCR,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.snapshot_repository import (
    SnapshotRepository,
)
from taiwan_geodoc_hub.infrastructure.adapters.firestore.snapshot_adapter import (
    SnapshotAdapter,
)
from taiwan_geodoc_hub.modules.access_managing.domain.ports.token_service import (
    TokenService,
)
from taiwan_geodoc_hub.infrastructure.adapters.http.token_adapter import TokenAdapter
from taiwan_geodoc_hub.modules.access_managing.domain.ports.credential_repository import (
    CredentialRepository,
)
from taiwan_geodoc_hub.infrastructure.adapters.fs.credential_adapter import (
    CredentialAdapter,
)
from taiwan_geodoc_hub.modules.access_managing.domain.ports.auth_service import (
    AuthService,
)
from taiwan_geodoc_hub.infrastructure.adapters.browser.auth_adapter import AuthAdapter
from taiwan_geodoc_hub.infrastructure.utils.hashers.bytes_hasher import BytesHasher
from taiwan_geodoc_hub.infrastructure.utils.generators.request_id_generator import (
    RequestIdGenerator,
)
from logging import Logger, LoggerAdapter
from injector import CallableProvider
from taiwan_geodoc_hub.infrastructure.constants.types import RequestId, UserId, TenantId


@asynccontextmanager
async def lifespan(app: Optional[Starlette] = None):
    try:
        get_app()
    except Exception:
        initialize_app(
            credential=Certificate(
                dict(
                    type="service_account",
                    project_id=getenv("PROJECT_ID"),
                    private_key=sub(r"\\n", "\n", getenv("PRIVATE_KEY")),
                    client_email=getenv("CLIENT_EMAIL"),
                    token_uri="https://oauth2.googleapis.com/token",
                )
            )
        )
    basicConfig(
        level=INFO,
        format="%(message)s",
        handlers=[StreamHandler()],
    )
    root_logger = getLogger()
    for handler in root_logger.handlers:
        handler.setFormatter(CloudLoggingJSONFormatter())
    getLogger("vellox.lifespan").setLevel(WARNING)
    getLogger("vellox.http").setLevel(WARNING)
    getLogger("werkzeug").setLevel(WARNING)
    injector = Injector()
    injector.binder.bind(UserDao, to=ClassProvider(UserAdapter))
    injector.binder.bind(AsyncClient, to=InstanceProvider(client()))
    injector.binder.bind(OCRResultRepository, to=ClassProvider(OCRResultAdapter))
    injector.binder.bind(RegistrationRepository, to=ClassProvider(RegistrationAdapter))
    injector.binder.bind(RoleDao, to=ClassProvider(RoleAdapter))
    injector.binder.bind(TenantDao, to=ClassProvider(TenantAdapter))
    injector.binder.bind(
        OCRProcessor, to=InstanceProvider(OCRSpace(api_key=getenv("OCR_SPACE_API_KEY")))
    )
    injector.binder.bind(CachedOCRProcessor, to=ClassProvider(PerformOCR))
    injector.binder.bind(SnapshotRepository, to=ClassProvider(SnapshotAdapter))
    injector.binder.bind(TokenService, to=ClassProvider(TokenAdapter))
    injector.binder.bind(CredentialRepository, to=ClassProvider(CredentialAdapter))
    injector.binder.bind(AuthService, to=ClassProvider(AuthAdapter))
    injector.binder.bind(RequestIdGenerator, to=ClassProvider(RequestIdGenerator))
    injector.binder.bind(BytesHasher, to=ClassProvider(BytesHasher))

    def create_logger():
        nonlocal injector
        requestId: Optional[str] = None
        userId: Optional[str] = None
        tenantId: Optional[str] = None
        try:
            requestId = injector.get(RequestId)
            userId = injector.get(UserId)
            tenantId = injector.get(TenantId)
        except Exception:
            pass
        logger = LoggerAdapter(
            getLogger(requestId),
            dict(
                userId=userId,
                tenantId=tenantId,
            ),
        )
        return logger

    injector.binder.bind(
        Logger,
        to=CallableProvider(create_logger),
    )
    if app is None:
        yield injector
    else:
        app.state.injector = injector
        yield
    delete_app(get_app())

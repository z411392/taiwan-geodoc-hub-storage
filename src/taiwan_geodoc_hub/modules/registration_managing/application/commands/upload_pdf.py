from injector import inject
from taiwan_geodoc_hub.modules.registration_managing.domain.services.pdf_validator import (
    PDFValidator,
)
from google.cloud.firestore import AsyncClient, AsyncTransaction, async_transactional
from logging import Logger
from taiwan_geodoc_hub.modules.registration_managing.domain.services.text_ripper import (
    TextRipper,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.services.registration_splitter import (
    RegistrationSplitter,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.registration_repository import (
    RegistrationRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.snapshot_repository import (
    SnapshotRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.snapshot import (
    Snapshot,
)
from taiwan_geodoc_hub.infrastructure.constants.tokens import (
    UserId,
    TenantId,
    SnapshotId,
)
from time import perf_counter
from taiwan_geodoc_hub.infrastructure.adapters.pubsub.event_publisher import (
    EventPublisher,
)
from taiwan_geodoc_hub.infrastructure.types.topic import Topic
from taiwan_geodoc_hub.modules.registration_managing.events.snapshot_uploaded import (
    SnapshotUploaded,
)
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.tenant_daily_usage_repository import (
    TenantDailyUsageRepository,
)
from taiwan_geodoc_hub.modules.registration_managing.dtos.tenant_daily_usage import (
    TenantDailyUsage,
)
from taiwan_geodoc_hub.modules.registration_managing.exceptions.tenant_max_snapshots_daily_limit_reached import (
    TenantMaxSnapshotsDailyLimitReached,
)
from datetime import datetime
from taiwan_geodoc_hub.infrastructure.utils.generators.trace_id_generator import (
    TraceIdGenerator,
)


class UploadPDF:
    _db: AsyncClient
    _split_registrations: RegistrationSplitter
    _rip_text: TextRipper
    _registration_repository: RegistrationRepository
    _snapshot_repository: SnapshotRepository
    _event_publisher: EventPublisher
    _logger: Logger
    _user_id: str
    _tenant_id: str
    _snapshot_id: str
    _validate_pdf: PDFValidator
    _tenant_daily_usage_repository: TenantDailyUsageRepository
    _next_trace_id: TraceIdGenerator

    @inject
    def __init__(
        self,
        /,
        db: AsyncClient,
        split_registrations: RegistrationSplitter,
        rip_text: TextRipper,
        registration_repository: RegistrationRepository,
        snapshot_repository: SnapshotRepository,
        tenant_daily_usage_repository: TenantDailyUsageRepository,
        event_publisher: EventPublisher,
        logger: Logger,
        user_id: UserId,
        tenant_id: TenantId,
        snapshot_id: SnapshotId,
        validate_pdf: PDFValidator,
        nextTraceId: TraceIdGenerator,
    ):
        self._db = db
        self._split_registrations = split_registrations
        self._rip_text = rip_text
        self._registration_repository = registration_repository
        self._snapshot_repository = snapshot_repository
        self._tenant_daily_usage_repository = tenant_daily_usage_repository
        self._event_publisher = event_publisher
        self._logger = logger
        self._user_id = user_id
        self._tenant_id = tenant_id
        self._snapshot_id = snapshot_id
        self._validate_pdf = validate_pdf
        self._next_trace_id = nextTraceId

    async def _load_or_create_new_tenant_daily_usage(
        self,
        date: str,
        /,
        transaction: AsyncTransaction,
    ):
        tenant_daily_usage = await self._tenant_daily_usage_repository.load(
            date,
            uow=transaction,
        )
        if tenant_daily_usage is None:
            tenant_daily_usage = TenantDailyUsage(
                id=date,
                snapshots=0,
            )
        return tenant_daily_usage

    async def _check_tenant_daily_usage(
        self,
        date: str,
        tenant_daily_usage: TenantDailyUsage,
        /,
        transaction: AsyncTransaction,
    ):
        if tenant_daily_usage["snapshots"] >= 10:
            raise TenantMaxSnapshotsDailyLimitReached(
                tenant_id=self._tenant_id,
                date=date,
            )
        tenant_daily_usage["snapshots"] += 1
        await self._tenant_daily_usage_repository.save(
            date,
            tenant_daily_usage,
            uow=transaction,
        )

    async def _create_snapshot_if_not_exists(
        self, pdf: bytes, /, transaction: AsyncTransaction
    ):
        await self._snapshot_repository.save(
            self._snapshot_id,
            Snapshot(
                id=self._snapshot_id,
            ),
            uow=transaction,
        )
        full_text = await self._rip_text(pdf=pdf)
        for registration in self._split_registrations(full_text):
            await self._registration_repository.save(
                registration.get("id"),
                registration,
                uow=transaction,
            )

    async def __call__(
        self,
        name: str,
        pdf: bytes,
    ):
        start = perf_counter()
        try:
            self._validate_pdf(pdf)

            @async_transactional
            async def run_in_transaction(transaction: AsyncTransaction):
                date = datetime.now().strftime("%Y-%m-%d")
                snapshot_exists = await self._snapshot_repository.exists(
                    self._snapshot_id,
                    uow=transaction,
                )
                tenant_daily_usage = await self._load_or_create_new_tenant_daily_usage(
                    date,
                    transaction=transaction,
                )
                if not snapshot_exists:
                    await self._create_snapshot_if_not_exists(
                        pdf,
                        transaction=transaction,
                    )
                await self._check_tenant_daily_usage(
                    date,
                    tenant_daily_usage,
                    transaction=transaction,
                )
                trace_id = await self._event_publisher.publish(
                    Topic.SnapshotUploaded,
                    SnapshotUploaded.ensure(
                        dict(
                            userId=self._user_id,
                            tenantId=self._tenant_id,
                            snapshotId=self._snapshot_id,
                            name=name,
                        )
                    ),
                )
                return trace_id

            trace_id: str = await run_in_transaction(self._db.transaction())
            self._logger.info(
                "UploadPDF finished", extra=dict(elapsed=perf_counter() - start)
            )
            return trace_id
        except Exception:
            self._logger.exception(
                "UploadPDF failed",
            )
            raise

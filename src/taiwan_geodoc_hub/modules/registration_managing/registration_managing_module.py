from injector import Module, ClassProvider, Provider
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.tenant_daily_usage_repository import (
    TenantDailyUsageRepository,
)
from taiwan_geodoc_hub.infrastructure.adapters.firestore.tenant_daily_usage_adapter import (
    TenantDailyUsageAdapter,
)
from taiwan_geodoc_hub.modules.system_maintaining.application.policies.read_through_cache_policy import (
    ReadThroughCachePolicy,
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

from taiwan_geodoc_hub.modules.registration_managing.domain.ports.ocr_service import (
    OCRService,
)
from taiwan_geodoc_hub.infrastructure.adapters.http.ocr_space import OCRSpace
from taiwan_geodoc_hub.modules.registration_managing.domain.ports.snapshot_repository import (
    SnapshotRepository,
)
from taiwan_geodoc_hub.infrastructure.adapters.firestore.snapshot_adapter import (
    SnapshotAdapter,
)
from taiwan_geodoc_hub.infrastructure.utils.hashers.bytes_hasher import BytesHasher


class OCRServiceProvider(Provider[OCRService]):
    def get(self, injector):
        read_through_cache_policy = injector.get(ReadThroughCachePolicy)
        func = injector.get(OCRSpace)
        ocr_result_repository = injector.get(OCRResultRepository)
        hash_bytes = injector.get(BytesHasher)

        async def compute_key(image: bytes):
            return hash_bytes(image)

        return read_through_cache_policy(
            func,
            repository=ocr_result_repository,
            compute_key=compute_key,
        )


class RegistrationManagingModule(Module):
    def configure(self, binder):
        binder.bind(OCRResultRepository, to=ClassProvider(OCRResultAdapter))
        binder.bind(RegistrationRepository, to=ClassProvider(RegistrationAdapter))
        binder.bind(
            OCRService,
            to=OCRServiceProvider(),
        )
        binder.bind(SnapshotRepository, to=ClassProvider(SnapshotAdapter))
        binder.bind(
            TenantDailyUsageRepository, to=ClassProvider(TenantDailyUsageAdapter)
        )

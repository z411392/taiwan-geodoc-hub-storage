from injector import Module, ClassProvider
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
from taiwan_geodoc_hub.modules.access_managing.domain.ports.role_dao import (
    RoleDao,
)
from taiwan_geodoc_hub.infrastructure.adapters.firestore.role_adapter import RoleAdapter
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


class AccessManagingModule(Module):
    def configure(self, binder):
        binder.bind(UserDao, to=ClassProvider(UserAdapter))
        binder.bind(TenantDao, to=ClassProvider(TenantAdapter))
        binder.bind(RoleDao, to=ClassProvider(RoleAdapter))
        binder.bind(CredentialRepository, to=ClassProvider(CredentialAdapter))
        binder.bind(AuthService, to=ClassProvider(AuthAdapter))

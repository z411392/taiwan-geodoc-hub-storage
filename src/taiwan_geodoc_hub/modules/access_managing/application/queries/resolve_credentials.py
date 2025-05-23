from operator import itemgetter
from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.credential_repository import (
    CredentialRepository,
)
from taiwan_geodoc_hub.modules.access_managing.domain.ports.auth_service import (
    AuthService,
)
from taiwan_geodoc_hub.modules.access_managing.dtos.credentials import (
    Credentials,
)
from taiwan_geodoc_hub.infrastructure.adapters.http.google_securetoken_api import (
    GoogleSecureTokenApi,
)
from taiwan_geodoc_hub.modules.access_managing.domain.services.is_token_valid import (
    is_token_valid,
)


class ResolveCredentials:
    _google_secure_token_api: GoogleSecureTokenApi
    _credential_repository: CredentialRepository
    _auth_service: AuthService

    @inject
    def __init__(
        self,
        /,
        google_secure_token_api: GoogleSecureTokenApi,
        credential_repository: CredentialRepository,
        auth_service: AuthService,
    ):
        self._google_secure_token_api = google_secure_token_api
        self._credential_repository = credential_repository
        self._auth_service = auth_service

    async def __call__(self) -> Credentials:
        existing_one = await self._credential_repository.load()
        if existing_one:
            id_token, refresh_token = itemgetter("idToken", "refreshToken")(
                existing_one
            )
            if is_token_valid(id_token):
                return existing_one
            refreshed_one = await self._google_secure_token_api.refresh_token(
                refresh_token
            )
            if refreshed_one:
                await self._credential_repository.save(refreshed_one)
                return refreshed_one
        new_one = await self._auth_service.auth()
        if new_one:
            await self._credential_repository.save(new_one)
        return new_one

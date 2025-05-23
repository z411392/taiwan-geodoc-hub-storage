from operator import itemgetter
from injector import inject
from taiwan_geodoc_hub.modules.access_managing.domain.ports.token_service import (
    TokenService,
)
from taiwan_geodoc_hub.modules.access_managing.domain.ports.credential_repository import (
    CredentialRepository,
)
from taiwan_geodoc_hub.modules.access_managing.domain.ports.auth_service import (
    AuthService,
)
from taiwan_geodoc_hub.modules.access_managing.dtos.credentials import (
    Credentials,
)


class ResolveCredentials:
    @inject
    def __init__(
        self,
        /,
        token_service: TokenService,
        credential_repository: CredentialRepository,
        auth_service: AuthService,
    ):
        self._token_service = token_service
        self._credential_repository = credential_repository
        self._auth_service = auth_service

    async def __call__(self) -> Credentials:
        existing_one = await self._credential_repository.load()
        if existing_one:
            id_token, refresh_token = itemgetter("idToken", "refreshToken")(
                existing_one
            )
            if self._token_service.is_token_valid(id_token):
                return existing_one
            refreshed_one = await self._token_service.refresh_token(refresh_token)
            if refreshed_one:
                await self._credential_repository.save(refreshed_one)
                return refreshed_one
        new_one = await self._auth_service.auth()
        if new_one:
            await self._credential_repository.save(new_one)
        return new_one

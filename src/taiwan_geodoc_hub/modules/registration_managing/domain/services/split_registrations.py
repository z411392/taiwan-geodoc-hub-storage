from taiwan_geodoc_hub.modules.registration_managing.domain.factories.registration_factory import (
    RegistrationFactory,
)
from re import split
from injector import inject
from taiwan_geodoc_hub.infrastructure.constants.types import UserId


class SplitRegistrations:
    _registration_factory: RegistrationFactory
    _user_id: UserId

    @inject
    def __init__(self, /, registration_factory: RegistrationFactory, user_id: UserId):
        self._registration_factory = registration_factory
        self._user_id = user_id

    def __call__(self, full_text: str):
        for text in split("〈 本謄本列印完畢 〉", full_text):
            registration = self._registration_factory(text=text, user_id=self._user_id)
            if registration is None:
                continue
            yield registration

import pytest
from injector import Injector
from taiwan_geodoc_hub.modules.access_managing.domain.ports.user_dao import (
    UserDao,
)
from os import getenv


# @pytest.mark.skip(reason="")
class TestUserDao:
    @pytest.fixture(scope="module")
    def user_dao(self, injector: Injector):
        return injector.get(UserDao)

    @pytest.mark.describe("要能夠解析 id_token")
    @pytest.mark.asyncio
    async def test_user_from_id_token(self, user_dao: UserDao):
        id_token = getenv("ID_TOKEN")
        user = await user_dao.from_id_token(id_token)
        assert user is not None

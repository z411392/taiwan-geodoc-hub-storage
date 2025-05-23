import pytest
from taiwan_geodoc_hub.infrastructure.utils.environments import (
    is_testing,
    is_developing,
    is_emulating,
)


# @pytest.mark.skip(reason="")
class TestEnvironmentsHelper:
    @pytest.mark.describe("要能夠判斷是否正在執行測試")
    def test_is_testing(self):
        assert is_testing()

    @pytest.mark.describe("要能夠判斷是否為 dev 環境")
    def test_is_developing(self):
        assert is_developing()

    @pytest.mark.describe("要能夠判斷是否正在模擬器環境下執行")
    def test_is_emulating(self):
        assert not is_emulating()

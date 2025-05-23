import pytest
from injector import Injector
from taiwan_geodoc_hub.infrastructure.adapters.pubsub.event_publisher import (
    EventPublisher,
)
from taiwan_geodoc_hub.infrastructure.types.topic import Topic
from taiwan_geodoc_hub.modules.registration_managing.events.snapshot_uploaded import (
    SnapshotUploaded,
)
from os import getenv


# @pytest.mark.skip(reason="")
class TestEventPublisher:
    @pytest.fixture(scope="module")
    def event_publisher(self, injector: Injector):
        return injector.get(EventPublisher)

    @pytest.mark.describe("要能夠發布事件")
    @pytest.mark.asyncio
    async def test_publish_event(
        self,
        event_publisher: EventPublisher,
    ):
        user_id = getenv("USER_ID")
        tenant_id = getenv("TENANT_ID")
        snapshot_id = getenv("SNAPSHOT_ID")
        trace_id = await event_publisher.publish(
            Topic.SnapshotUploaded,
            SnapshotUploaded.ensure(
                dict(
                    userId=user_id,
                    tenantId=tenant_id,
                    snapshotId=snapshot_id,
                    name="建物謄本.pdf",
                )
            ),
        )
        assert trace_id is not None

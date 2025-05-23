from injector import inject
from google.cloud.pubsub import PublisherClient
from asyncio import wrap_future
from taiwan_geodoc_hub.infrastructure.types.topic import Topic
from json import dumps
from taiwan_geodoc_hub.infrastructure.utils.generators.trace_id_generator import (
    TraceIdGenerator,
)


class EventPublisher:
    _pubsub: PublisherClient
    _nextTraceId: TraceIdGenerator

    @inject
    def __init__(
        self,
        /,
        pubsub: PublisherClient,
        next_trace_id: TraceIdGenerator,
    ):
        self._pubsub = pubsub
        self._next_trace_id = next_trace_id

    async def publish(self, topic: Topic, payload: dict):
        trace_id = self._next_trace_id(to_base62=False)
        attributes = dict(
            namespace=trace_id,
        )
        data = bytes(dumps(payload), "utf-8")
        await wrap_future(self._pubsub.publish(str(topic), data, **attributes))
        return trace_id

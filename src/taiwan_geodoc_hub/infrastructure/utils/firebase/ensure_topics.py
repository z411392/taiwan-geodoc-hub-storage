from asyncio import get_running_loop
from google.cloud.pubsub import PublisherClient
from taiwan_geodoc_hub.infrastructure.types.topic import Topic
from google.api_core.exceptions import AlreadyExists


async def ensure_topics(pubsub: PublisherClient):
    for topic in Topic:
        try:
            await get_running_loop().run_in_executor(
                None,
                lambda: pubsub.create_topic(
                    request=dict(name=str(topic)),
                ),
            )
        except AlreadyExists:
            continue

from uuid import uuid1, uuid4, uuid5
from shortuuid import encode


class RequestIdGenerator:
    def __call__(self):
        return encode(uuid5(uuid1(), str(uuid4())))

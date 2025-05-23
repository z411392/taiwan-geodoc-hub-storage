from dataclasses import dataclass, asdict
from dacite import from_dict


@dataclass
class ExecutionCompleted:
    @classmethod
    def from_dict(cls, data):
        return from_dict(data_class=cls, data=data)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def ensure(cls, data):
        return cls.from_dict(data).to_dict()

from taiwan_geodoc_hub.infrastructure.utils.classes.bloc import Bloc
from typing import Union
from taiwan_geodoc_hub.modules.system_maintaining.events.execution_completed import (
    ExecutionCompleted,
)
from taiwan_geodoc_hub.modules.system_maintaining.events.execution_failed import (
    ExecutionFailed,
)
from typing import Literal
from dataclasses import dataclass, asdict
from dacite import from_dict


@dataclass(frozen=True, eq=True)
class Completed:
    status: Literal["completed"] = "completed"

    def resolve(self):
        return self

    def reject(self, reason: str):
        return self

    @classmethod
    def from_dict(cls, data: dict):
        return from_dict(data_class=cls, data=data)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def ensure(cls, data):
        return cls.from_dict(data).to_dict()


@dataclass(frozen=True, eq=True)
class Failed:
    reason: str
    status: Literal["failed"] = "failed"

    def __init__(self, reason: str):
        self.reason = reason

    def resolve(self):
        return self

    def reject(self, reason: str):
        return self

    @classmethod
    def from_dict(cls, data: dict):
        return from_dict(data_class=cls, data=data)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def ensure(cls, data):
        return cls.from_dict(data).to_dict()


@dataclass(frozen=True, eq=True)
class Progressing:
    status: Literal["progressing"] = "progressing"

    def resolve(self):
        return Completed()

    def reject(self, reason: str):
        return Failed(reason)

    @classmethod
    def from_dict(cls, data: dict):
        return from_dict(data_class=cls, data=data)


Event = Union[ExecutionCompleted, ExecutionFailed]

State = Union[Progressing, Completed, Failed]


class ProjectingProcessManager(Bloc[Event, State]):
    def __init__(self, initial_state: State):
        super().__init__(initial_state)
        self.on(ExecutionCompleted, self._apply_execution_completed)
        self.on(ExecutionFailed, self._apply_execution_failed)

    async def _apply_execution_completed(self, payload: ExecutionCompleted):
        self.emit(self.state.resolve())

    async def _apply_execution_failed(self, payload: ExecutionFailed):
        self.emit(self.state.reject(payload.reason))

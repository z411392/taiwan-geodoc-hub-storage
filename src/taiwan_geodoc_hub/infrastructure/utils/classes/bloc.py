from typing import TypeVar, Generic, Callable, Awaitable, Dict, Type, Any
from reactivex.subject import ReplaySubject
from dataclasses import is_dataclass

Event = TypeVar("Event", bound=Any)
State = TypeVar("State", bound=Any)


class StateMustBeADataClass(Exception):
    def __init__(self):
        pass

    def __iter__(self):
        yield "name", __class__.__name__


class Bloc(Generic[Event, State]):
    _state: State
    _state_subject: ReplaySubject
    _handlers: Dict[Type[Event], Callable[[Event], Awaitable[State]]]

    def __init__(self, initial_state: State):
        if not is_dataclass(initial_state):
            raise StateMustBeADataClass()
        self._state: State = initial_state
        self._state_subject: ReplaySubject = ReplaySubject(1)
        self._handlers: Dict[Type[Event], Callable[[Event], Awaitable[State]]] = {}
        self._state_subject.on_next(self._state)

    @property
    def state(self) -> State:
        return self._state

    def emit(self, new_state: State):
        if not is_dataclass(new_state):
            raise StateMustBeADataClass()
        if new_state == self._state:
            return
        self._state = new_state
        self._state_subject.on_next(new_state)
        return

    def on(
        self,
        event_type: Type[Event],
        handler: Callable[[Event], Awaitable[State]],
    ):
        self._handlers[event_type] = handler

    async def add(self, event: Event):
        handler = self._handlers.get(type(event))
        if not handler:
            return
        await handler(event)

    def subscribe(self, callback: Callable[[State], Any]):
        disposable = self._state_subject.subscribe(callback)

        async def unsubscribe():
            disposable.dispose()

        return unsubscribe

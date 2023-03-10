from queue import Queue
from abc import ABC, abstractclassmethod

from customevents import CustomEvent

class Listener(ABC):
    
    def __init__(self, events: list[str], id: str) -> None:
        self.events_that_i_need_to_listen_to: list[str] = events
        self.id: str = id

        EventManager.upsert_listener(self)

    @abstractclassmethod
    def notify(self, ce: CustomEvent) -> None: ...

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Listener) and self.id == __o.id

    def __hash__(self) -> int:
        return hash(self.id)

class EventManager:
    
    listeners: dict[str, set[Listener]] = dict()
    event_queue: Queue[CustomEvent] = Queue()
    
    def initialize(custom_events: list[str]) -> None:
        for ce_key in custom_events:
            EventManager.listeners[ce_key] = set()

    def flush() -> None:
        while not EventManager.event_queue.empty():
            ce = EventManager.event_queue.get()
            for listener in EventManager.listeners[ce.key]:
                listener.notify(ce)

    def upsert_listener(listener: Listener) -> None:
        for ce_key in listener.events_that_i_need_to_listen_to:
            if listener in EventManager.listeners[ce_key]:
                EventManager.listeners[ce_key].remove(listener)
            EventManager.listeners[ce_key].add(listener)

    def push_event(ce: CustomEvent) -> None:
        EventManager.event_queue.put(ce)

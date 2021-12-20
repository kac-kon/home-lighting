from threading import Thread, Event
from typing import Optional, Any, List


class Monitoring:
    def __init__(self, function: Optional[Any] = None, args: Optional[List[Any]] = None):
        if args is None:
            args = []
        self._target = function
        self._args = args
        self._event = Event()
        self._thread = Thread(target=self._target, args=self._args)

    def start_monitoring(self, function: Optional[Any] = None, args: Optional[List[Any]] = None):
        if args is None:
            args = []
        self.set_target(function, args)
        if self.is_thread_alive():
            self.stop_monitoring()
            self.clear_event()
            self.start_thread()
        else:
            self.clear_event()
            self.start_thread()

    def stop_monitoring(self):
        if self.is_thread_alive():
            self.set_event()
            self.join_thread()

    def set_target(self, function: Any = None, args: Optional[List[Any]] = None):
        if args is None:
            args = []
        if function is not None:
            self._target = function
        self._args = args

    def is_thread_alive(self) -> bool:
        return self._thread.is_alive()

    def is_event_set(self) -> bool:
        return self._event.is_set()

    def set_event(self) -> None:
        self._event.set()

    def clear_event(self) -> None:
        self._event.clear()

    def start_thread(self) -> None:
        self._thread = Thread(target=self._target, args=self._args)
        self._thread.start()

    def join_thread(self, timeout: Optional[float] = None) -> None:
        self._thread.join(timeout)

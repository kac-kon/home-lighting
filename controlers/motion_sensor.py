import time
from threading import Thread, Event

import RPi.GPIO as GPIO
from initials.constants import GPIO as INITS


class MotionSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._motion = INITS.GPIO_MOTION
        GPIO.setup(self._motion, GPIO.IN)

        self._monitoring_thread = Thread()
        self._monitoring_event = Event()
        self._callbacks = []

    def __del__(self):
        GPIO.cleanup()

    def is_motion_active(self) -> bool:
        return GPIO.input(self._motion)

    def _monitor_activity(self) -> None:
        while not self._monitoring_event.is_set():
            if self.is_motion_active():
                self._notify_observer()
            time.sleep(.1)

    def _monitor_activity_timed(self, timeout: float) -> None:
        while not self._monitoring_event.is_set():
            print(self.is_motion_active())
            if self.is_motion_active():
                self._notify_observer()
                time.sleep(timeout)
            time.sleep(.1)

    def register_motion_callback(self, callback: object) -> None:
        self._callbacks.append(callback)

    def _notify_observer(self) -> None:
        for callback in self._callbacks:
            callback()

    def start_monitoring(self):
        print("starting monitoring motion")
        if self._monitoring_thread.is_alive():
            self._monitoring_event.set()
            self._monitoring_thread.join()
            self._monitoring_event.clear()
            self._monitoring_thread = Thread(target=self._monitor_activity)
            self._monitoring_thread.start()
        else:
            self._monitoring_event.clear()
            self._monitoring_thread = Thread(target=self._monitor_activity)
            self._monitoring_thread.start()
        print("started monitoring motion")

    def start_timed_monitoring(self, timeout: float) -> None:
        if self._monitoring_thread.is_alive():
            self._monitoring_event.set()
            self._monitoring_thread.join()
            self._monitoring_event.clear()
            self._monitoring_thread = Thread(target=self._monitor_activity_timed, args=[timeout])
        else:
            self._monitoring_event.clear()
            self._monitoring_thread = Thread(target=self._monitor_activity_timed, args=[timeout])
            self._monitoring_thread.run()

    def stop_monitoring(self):
        self._monitoring_event.set()
        self._monitoring_thread.join()

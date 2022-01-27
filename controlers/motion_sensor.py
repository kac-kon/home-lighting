import RPi.GPIO as GPIO
import time

from controlers.monitoring import Monitoring
from initials.constants import GPIO as INITS


class MotionSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._motion = INITS.GPIO_MOTION
        GPIO.setup(self._motion, GPIO.IN)

        self._monitoring = Monitoring(self._monitor_activity)
        self._callbacks = []

    def __del__(self):
        GPIO.cleanup()

    def is_motion_active(self) -> bool:
        return GPIO.input(self._motion)

    def is_monitored(self) -> bool:
        return self._monitoring.is_thread_alive()

    def _monitor_activity(self) -> None:
        while not self._monitoring.is_event_set():
            if self.is_motion_active():
                self._notify_observer()
            time.sleep(.5)

    def register_motion_observer(self, callback: object) -> None:
        self._callbacks.append(callback)

    def _notify_observer(self) -> None:
        for callback in self._callbacks:
            callback()

    def start_monitoring(self):
        print("starting monitoring motion")
        self._monitoring.start_monitoring()
        print("started monitoring motion")

    def stop_monitoring(self):
        self._monitoring.stop_monitoring()

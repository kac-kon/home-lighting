import RPi.GPIO as GPIO
import time

from controlers.monitoring import Monitoring
from initials.constants import GPIO as INITS


class DistanceSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._trigger = INITS.GPIO_TRIGGER
        self._echo = INITS.GPIO_ECHO
        self._delta = 5
        self.distance = 0
        self.threshold = 3

        GPIO.setup(self._trigger, GPIO.OUT)
        GPIO.setup(self._echo, GPIO.IN)

        self._callbacks = []
        self._monitoring = Monitoring(self.get_distance)

    def __del__(self):
        GPIO.cleanup()

    def is_monitored(self) -> bool:
        return self._monitoring.is_thread_alive()

    def get_distance(self):
        while not self._monitoring.is_event_set():
            GPIO.output(self._trigger, True)

            time.sleep(0.00001)
            GPIO.output(self._trigger, False)

            start_time = time.time()
            stop_time = time.time()

            while GPIO.input(self._echo) == 0:
                start_time = time.time()

            while GPIO.input(self._echo) == 1:
                stop_time = time.time()

            time_elapsed = stop_time - start_time
            distance = int((time_elapsed * 34300) / 2)

            if abs(self.distance - distance) > self.threshold and distance < 300:
                self.distance = distance
                self._notify_observers()
                time.sleep(.3)

            time.sleep(.2)

    def register_distance_observer(self, callback: object):
        self._callbacks.append(callback)

    def _notify_observers(self):
        for callback in self._callbacks:
            callback()

    def start_monitoring(self):
        print("starting monitoring distance")
        self._monitoring.start_monitoring()
        print("started monitoring distance")

    def stop_monitoring(self):
        self._monitoring.stop_monitoring()

import RPi.GPIO as GPIO
import time

from controlers.monitoring import Monitoring
from initials.constants import GPIO as INITS


class LightSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._ldr = INITS.GPIO_LDR

        self.value = 0
        self.lights_on = False

        self._monitoring = Monitoring(self.read_time)
        self._callbacks = []

    def __del__(self):
        GPIO.cleanup()

    def is_monitored(self) -> bool:
        return self._monitoring.is_thread_alive()

    def read_time(self) -> None:
        print("light sensor read init")
        while not self._monitoring.is_event_set():
            count = 0
            GPIO.setup(self._ldr, GPIO.OUT)
            GPIO.output(self._ldr, False)
            time.sleep(.1)
            GPIO.setup(self._ldr, GPIO.IN)

            while GPIO.input(self._ldr) == 0:
                count += 1
                time.sleep(.001)

            self.value = count
            lights_on = False if count > 170 else True
            if lights_on != self.lights_on:
                self.lights_on = lights_on
                self._notify_observer()
            time.sleep(.3)

    def register_lighting_observer(self, callback: object) -> None:
        self._callbacks.append(callback)

    def _notify_observer(self) -> None:
        for callback in self._callbacks:
            callback()

    def start_monitoring(self):
        print("starting monitoring lights")
        self._monitoring.start_monitoring()
        print("started monitoring lights")

    def stop_monitoring(self):
        self._monitoring.stop_monitoring()

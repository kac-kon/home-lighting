from threading import Event, Thread

import RPi.GPIO as GPIO
import time
from initials.constants import GPIO as INITS


class LightSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self._ldr = INITS.GPIO_LDR

        self.value = 0
        self.lights_off = False

        self._monitoring_thread = Thread()
        self._monitoring_event = Event()
        self._callbacks = []

    def __del__(self):
        GPIO.cleanup()

    def read_time(self) -> None:
        print("light sensor read init")
        while not self._monitoring_event.is_set():
            count = 0
            GPIO.setup(self._ldr, GPIO.OUT)
            GPIO.output(self._ldr, False)
            time.sleep(.1)
            GPIO.setup(self._ldr, GPIO.IN)

            while GPIO.input(self._ldr) == 0:
                count += 1

            self.value = count
            self.lights_off = False if count > 150000 else True
            print(self.lights_off)
            time.sleep(.3)


    def register_lighting_observer(self, callback: object) -> None:
        self._callbacks.append(callback)

    def _notify_observer(self) -> None:
        for callback in self._callbacks:
            callback()

    def start_monitoring(self):
        if self._monitoring_thread.is_alive():
            self._monitoring_event.set()
            self._monitoring_thread.join()
            self._monitoring_event.clear()
            self._monitoring_thread = Thread(target=self.read_time)
            self._monitoring_thread.run()
        else:
            self._monitoring_event.clear()
            self._monitoring_thread = Thread(target=self.read_time)
            self._monitoring_thread.run()


    def stop_monitoring(self):
        self._monitoring_event.set()
        self._monitoring_thread.join()

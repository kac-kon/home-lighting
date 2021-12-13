import time
from threading import Event, Thread

from typing import Dict

from controlers.led_control import LED
from controlers.spectrum import Spec
from controlers.distance_sensor import DistanceSensor
from controlers.light_sensor import LightSensor
from controlers.motion_sensor import MotionSensor


class Orchestrator:
    def __init__(self):
        self._led = LED()
        self._spec = Spec(self._led)
        self._distance = DistanceSensor()
        self._light = LightSensor()
        self._motion = MotionSensor()

        self._motion.register_motion_callback(self._motion_observer)
        self._motion_event = Event()
        self._motion_thread = Thread()
        self._motion_start_time = 0
        self._leds_off = True
        self._motion_timer = 20 * 2

    def start_auto_led(self):
        self._spec.start_auto()

    def stop_auto_led(self):
        self._spec.stop_auto()

    def set_colors(self, colors: list):
        self._led.set_color(colors)

    def set_strip_enable(self, strip: int, state: bool):
        self._led.set_enable_state(strip, state)

    def set_strip_brightness(self, brightness: int):
        self._led.set_brightness(brightness)

    def set_addressed_properties(self, properties: Dict[str, int]) -> None:
        """
        :param properties: required keys: direction, frequency, count
        :return: None
        """
        self._led.set_addressed(properties)

    def set_autoled_properties(self, properties: Dict[str, int]) -> None:
        """
        :param properties: required keys: sensitivity, inertia, frequency, fade_speed
        :return: None
        """
        self._spec.set_properties(properties)

    def get_led_state(self) -> dict:
        return self._led.get_led_state()

    def start_monitoring(self) -> None:
        print("starting monitoring")
        self._distance.start_monitoring()
        self._light.start_monitoring()
        self._motion.start_monitoring()
        print("started monitoring")

    def stop_monitoring(self) -> None:
        self._distance.stop_monitoring()
        self._light.stop_monitoring()
        self._motion.stop_monitoring()

    def lights_up(self):
        self.set_colors([255, 255, 255])
        self._leds_off = False

    def _wait_for_no_motion(self):
        count = 0
        print('timer started')
        while not self._motion_event.is_set():
            count += 1
            time.sleep(.5)
            print(count)
            if count >= self._motion_timer:
                break
        if count >= self._motion_timer:
            self.set_colors([0, 0, 0])
            self._leds_off = True

    def _motion_observer(self) -> None:
        print('motion detected')
        if not self._light.lights_on and time.time() > self._motion_start_time + 5:
            if self._leds_off and not self._motion_thread.is_alive():
                self.lights_up()
            if self._motion_thread.is_alive():
                self._motion_event.set()
                self._motion_thread.join()
                self._motion_event.clear()
            self._motion_thread = Thread(target=self._wait_for_no_motion)
            self._motion_start_time = time.time()
            self._motion_thread.start()
        else:
            self._motion_event.set()
            if self._motion_thread.is_alive():
                self._motion_thread.join()
            self._motion_event.clear()
            self.set_colors([0, 0, 0])
            self._leds_off = True

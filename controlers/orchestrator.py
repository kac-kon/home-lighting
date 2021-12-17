from typing import Dict

from controlers.led_control import LED
from controlers.sensors import Sensors
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
        self._sensors = Sensors(self, self._distance, self._light, self._motion)

        self.set_colors([255, 255, 255])

    @property
    def lights_on(self):
        return self._led.lights_on

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
        :param properties: accepted keys: direction, frequency, count
        :return: None
        """
        self._led.set_addressed(properties)

    def set_autoled_properties(self, properties: Dict[str, int]) -> None:
        """
        :param properties: accepted keys: sensitivity, inertia, frequency, fade_speed
        :return: None
        """
        self._spec.set_properties(properties)

    def get_led_state(self) -> dict:
        return self._led.get_led_state()

    def start_monitoring(self) -> None:
        self._distance.start_monitoring()
        self._light.start_monitoring()
        # self._motion.start_monitoring()

    def stop_monitoring(self) -> None:
        self._distance.stop_monitoring()
        self._light.stop_monitoring()
        self._motion.stop_monitoring()

    def lights_up(self):
        self.set_strip_enable(0, True)
        self.set_strip_enable(1, True)

    def lights_down(self):
        self.set_strip_enable(0, False)
        self.set_strip_enable(1, False)

    def switch_leds(self):
        if self.lights_on:
            self.lights_up()
        else:
            self.lights_down()

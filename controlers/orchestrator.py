from typing import Dict

from controlers.led_control import LED
from controlers.spectrum import Spec


class Orchestrator:
    def __init__(self):
        self._led = LED()
        self._spec = Spec(self._led)

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

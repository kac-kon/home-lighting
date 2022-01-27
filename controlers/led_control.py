from typing import List, Any, Dict

from controlers.monitoring import Monitoring
from initials import constants
from initials.variables import LedVar

import time
import pigpio
import threading
import random
from rpi_ws281x import *


class LED:
    def __init__(self):
        self._var = LedVar()
        self._pi = pigpio.pi()
        self._strip = Adafruit_NeoPixel(constants.LEDStrip.LED_COUNT,
                                        constants.LEDStrip.LED_PIN,
                                        constants.LEDStrip.LED_FREQ_HZ,
                                        constants.LEDStrip.LED_DMA,
                                        constants.LEDStrip.LED_INVERT,
                                        constants.LEDStrip.LED_BRIGHTNESS,
                                        constants.LEDStrip.LED_CHANNEL)
        self._strip.begin()
        random.seed()

        self._animation_monitoring = Monitoring()
        self._animation_speed = 1
        self._animation_timeout = 0.05
        self._animation_number = 0

        self._var.register_led_color_callback(self._catch_color_change)
        self._var.register_led_enable_callback(self._catch_enable_change)
        self._var.register_led_strip_callback(self._catch_strip_properties_change)

    @property
    def lights_on(self) -> bool:
        return self._var.led5_on and self._var.led12_on

    @staticmethod
    def random_colors() -> List[int]:
        c1 = random.randint(0, 1) * 255
        c2 = random.randint(0, 1) * 255
        c3 = random.randint(0, 1) * 255
        if c1 == c2 == c3 == 0:
            return [255, 255, 255]
        return [c1, c2, c3]

    def _catch_enable_change(self) -> None:
        self._set_color()

    def _catch_color_change(self) -> None:
        self._set_color()

    def _catch_strip_properties_change(self) -> None:
        self._v5_set_color()

    def _set_color(self) -> None:
        self._v12_set_color()
        self._v5_set_color()

    def _v12_set_color(self) -> None:
        if self._var.led12_on:
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_RED, int(
                self._var.led_red * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS))
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_GREEN, int(
                self._var.led_green * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS))
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_BLUE, int(
                self._var.led_blue * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS))
        else:
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_RED, 0)
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_GREEN, 0)
            self._pi.set_PWM_dutycycle(constants.GPIO.GPIO_BLUE, 0)

    def _v5_set_color(self) -> None:
        if self._var.led5_on:
            red = int(self._var.led_red * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS)
            green = int(self._var.led_green * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS)
            blue = int(self._var.led_blue * self._var.led_brightness / constants.INITIALS.LED_BRIGHTNESS)
            if self._var.led_strip_direction > 0:
                start = 0
                end = constants.LEDStrip.LED_COUNT
                step = 1
            else:
                start = constants.LEDStrip.LED_COUNT - 1
                end = -1
                step = -1
            for i in range(start, end, step):
                if abs(start - i) < self._var.led_strip_display and i % self._var.led_strip_direction == 0:
                    self._strip.setPixelColorRGB(i, red, green, blue)
                else:
                    self._strip.setPixelColorRGB(i, 0, 0, 0)
            self._strip.show()
        else:
            for i in range(0, self._var.led_strip_display, self._var.led_strip_direction):
                self._strip.setPixelColorRGB(i, 0, 0, 0)
            self._strip.show()

    def _fade_away(self) -> None:
        self._var.led_brightness = constants.INITIALS.LED_BRIGHTNESS
        time.sleep(0.1)
        while self._var.led_brightness > 0:
            if (self._var.led_brightness - self._var.fade_away_speed) < 0:
                self._var.led_brightness = 0
            else:
                self._var.led_brightness -= self._var.fade_away_speed
            time.sleep(.02)

    def fade_away(self) -> None:
        self._fade_away()

    def set_color(self, color_list: List[int]) -> None:
        self._var.led_red = color_list[0]
        self._var.led_green = color_list[1]
        self._var.led_blue = color_list[2]

    def set_enable_state(self, strip: int, state: bool) -> None:
        if strip == 0:
            self._var.led5_on = state
        elif strip == 1:
            self._var.led12_on = state

    def set_brightness(self, new_value: int) -> None:
        self._var.led_brightness = new_value

    def set_addressed(self, properties: Dict[str, int]) -> None:
        """
        :param properties: accepted keys: direction, frequency, count
        :return: None
        """
        if properties.keys().__contains__('direction') and properties.keys().__contains__('frequency'):
            direction: int = properties['direction']
            frequency: int = properties['frequency']
            self._var.led_strip_direction = direction * frequency
        elif properties.keys().__contains__('frequency'):
            frequency: int = properties['frequency']
            direction: int = -1 if self._var.led_strip_direction < 0 else 1
            self._var.led_strip_direction = direction * frequency
        elif properties.keys().__contains__('direction'):
            direction: int = properties['direction']
            frequency: int = abs(self._var.led_strip_direction)
            self._var.led_strip_direction = direction * frequency
        if properties.keys().__contains__('count'):
            self._var.led_strip_display = properties['count']

    def get_led_state(self) -> Dict[str, Any]:
        brightness = self._var.led_brightness
        red = self._var.led_red
        green = self._var.led_green
        blue = self._var.led_blue
        led5 = self._var.led5_on
        led12 = self._var.led12_on

        direction = -1 if self._var.led_strip_direction < 0 else 1
        led_freq = abs(self._var.led_strip_direction)
        led_count = self._var.led_strip_display
        addressed = [{"direction": direction, "frequency": led_freq, "count": led_count}]

        enabled = True if self._animation_monitoring.is_thread_alive() else False
        number = self._animation_number
        speed = self._animation_speed
        animation = [{"enabled": enabled, "number": number, "speed": speed}]

        keys = ["brightness", "red", "green", "blue", "led5", "led12", "addressed", "animation"]
        values = [brightness, red, green, blue, led5, led12, addressed, animation]

        return dict(zip(keys, values))

    def animation_one(self) -> None:
        """
        pulse animation
        """
        print('anim one started')
        while not self._animation_monitoring.is_event_set():
            for i in range(0, 256, self._animation_speed):
                if self._animation_monitoring.is_event_set():
                    break
                self.set_brightness(i)
                time.sleep(self._animation_timeout)
            for i in range(0, 256, self._animation_speed):
                if self._animation_monitoring.is_event_set():
                    break
                self.set_brightness(255-i)
                time.sleep(self._animation_timeout)

    def animation_two(self) -> None:
        """
        change rgb color
        """
        print('anim two started')
        while not self._animation_monitoring.is_event_set():
            for i in range(0, 256, self._animation_speed):
                if self._animation_monitoring.is_event_set():
                    break
                self.set_color([255-i, i, 0])
            for i in range(0, 256, self._animation_speed):
                if self._animation_monitoring.is_event_set():
                    break
                self.set_color([0, 255-i, i])
            for i in range(0, 256, self._animation_speed):
                if self._animation_monitoring.is_event_set():
                    break
                self.set_color([i, 0, 255-i])

    def animation_three(self) -> None:
        """
        change rgb multicolor
        """
        print('anim three started')
        while not self._animation_monitoring.is_event_set():
            for i in range(0, 256, self._animation_speed):
                if self._animation_monitoring.is_event_set():
                    break
                self.set_color([255-i, i, 255])
            for i in range(0, 256, self._animation_speed):
                if self._animation_monitoring.is_event_set():
                    break
                self.set_color([i, 255, 255-i])
            for i in range(0, 256, self._animation_speed):
                if self._animation_monitoring.is_event_set():
                    break
                self.set_color([255, 255-i, i])

    def set_animation(self, number: int) -> None:
        self._animation_number = number
        if number == 1:
            self._animation_monitoring.start_monitoring(self.animation_one)
        elif number == 2:
            self._animation_monitoring.start_monitoring(self.animation_two)
        elif number == 3:
            self._animation_monitoring.start_monitoring(self.animation_three)
        else:
            print('stopped animations')
            self._animation_monitoring.stop_monitoring()

    def set_animation_speed(self, speed: int) -> None:
        if speed < 1:
            speed = 1
        self._animation_speed = speed

from initials import constants


class LedVar:
    def __init__(self):
        self._led12_on = constants.INITIALS.LED12_ON
        self._led5_on = constants.INITIALS.LED5_ON
        self._led_brightness = constants.INITIALS.LED_BRIGHTNESS
        self._led_red = constants.INITIALS.LED_RED
        self._led_green = constants.INITIALS.LED_GREEN
        self._led_blue = constants.INITIALS.LED_BLUE
        self._led_strip_direction = constants.INITIALS.LED_STRIP_DIRECTION
        self._led_strip_display = constants.INITIALS.LED_STRIP_DISPLAY
        self._fade_away_speed = constants.INITIALS.FADE_AWAY_SPEED

        self._led_enable_callbacks = []
        self._led_color_callbacks = []
        self._led_strip_callbacks = []

    @property
    def fade_away_speed(self):
        return self._fade_away_speed

    @property
    def led12_on(self):
        return self._led12_on

    @led12_on.setter
    def led12_on(self, new_value):
        self._led12_on = new_value
        self._notify_led_enable_observer()

    @property
    def led5_on(self):
        return self._led5_on

    @led5_on.setter
    def led5_on(self, new_value):
        self._led5_on = new_value
        self._notify_led_enable_observer()

    @property
    def led_brightness(self):
        return self._led_brightness

    @led_brightness.setter
    def led_brightness(self, new_value):
        self._led_brightness = new_value
        self._notify_led_color_observer()

    @property
    def led_red(self):
        return self._led_red

    @led_red.setter
    def led_red(self, new_value):
        self._led_red = new_value
        self._notify_led_color_observer()

    @property
    def led_green(self):
        return self._led_green

    @led_green.setter
    def led_green(self, new_value):
        self._led_green = new_value
        self._notify_led_color_observer()

    @property
    def led_blue(self):
        return self._led_blue

    @led_blue.setter
    def led_blue(self, new_value):
        self._led_blue = new_value
        self._notify_led_color_observer()

    @property
    def led_strip_direction(self):
        return self._led_strip_direction

    @led_strip_direction.setter
    def led_strip_direction(self, new_value):
        if new_value < -10:
            new_value = -10
        elif new_value > 10:
            new_value = 10
        elif new_value == 0:
            new_value = 1
        self._led_strip_direction = new_value
        self._notify_led_strip_properties_observer()

    @property
    def led_strip_display(self):
        return self._led_strip_display

    @led_strip_display.setter
    def led_strip_display(self, new_value):
        if new_value > constants.LEDStrip.LED_COUNT:
            new_value = constants.LEDStrip.LED_COUNT
        self._led_strip_display = new_value
        self._notify_led_strip_properties_observer()

    def _notify_led_enable_observer(self):
        for callback in self._led_enable_callbacks:
            callback()

    def register_led_enable_callback(self, callback):
        self._led_enable_callbacks.append(callback)

    def _notify_led_color_observer(self):
        for callback in self._led_color_callbacks:
            callback()

    def register_led_color_callback(self, callback):
        self._led_color_callbacks.append(callback)

    def _notify_led_strip_properties_observer(self):
        for callback in self._led_strip_callbacks:
            callback()

    def register_led_strip_callback(self, callback):
        self._led_strip_callbacks.append(callback)

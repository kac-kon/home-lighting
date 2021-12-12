class State:

    def __init__(
            self,
            brightness=0,
            red=0,
            green=0,
            blue=0,
            led1=True,
            led2=True,
            auto_led=False,
            timer_enabled=False,
            timer_time=-1,
            led_direction=0,
            led_freq=1,
            led_count=180
    ):
        self.brightness = brightness
        self.red = red
        self.green = green
        self.blue = blue
        self.led1 = led1
        self.led2 = led2
        self.leds = True if (self.led1 == self.led2 is True) else False
        self.auto_led = auto_led
        self.timer = [{"enabled": timer_enabled, "time": timer_time}]
        self.addressed = [{"direction": led_direction, "frequency": led_freq, "count": led_count}]


if __name__ == "__main__":
    state = State(255, 127, 127, 127, True, True, True, True)
    print(state.__dict__)

    a = {"1": 2, "2": 3}
    b = {"3": 0}
    c = {**a, **b}
    print(c)

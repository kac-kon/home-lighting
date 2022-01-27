class State:

    def __init__(
            self,
            led_state: dict
    ):
        self.state = led_state


if __name__ == "__main__":
    brightness = 255
    red = 127
    green = 0
    blue = 60
    led5 = True
    led12 = False

    direction = -1
    led_freq = 2
    led_count = 180
    addressed = {"direction": direction, "frequency": led_freq, "count": led_count}

    enabled = False
    number = 0
    speed = 2
    animation = {"enabled": enabled, "number": number, "speed": speed}

    keys = ["brightness", "red", "green", "blue", "led5", "led12", "addressed", "animation"]
    values = [brightness, red, green, blue, led5, led12, addressed, animation]

    st = dict(zip(keys, values))
    state = State(st)
    print(state.__dict__)

    # a = {"1": 2, "2": 3}
    # b = {"3": 0}
    # c = {**a, **b}
    # print(c)

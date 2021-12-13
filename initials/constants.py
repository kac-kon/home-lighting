class GPIO:
    GPIO_RED = 17                               # GPIO pin for 12V red channel
    GPIO_GREEN = 22                             # GPIO pin for 12V green channel
    GPIO_BLUE = 27                              # GPIO pin for 12V blue channel
    GPIO_WS281B = 18                            # GPIO pin for WS281B addressable strip
    GPIO_W1 = 4                                 # GPIO pin for 1-wire interface
    GPIO_TRIGGER = 23
    GPIO_ECHO = 24
    GPIO_MOTION = 7
    GPIO_LDR = 25


class LEDStrip:
    LED_COUNT = 180                             # Number of LED pixels.
    LED_PIN = GPIO.GPIO_WS281B                  # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ = 800000                        # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10                                # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255                        # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False                          # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0                             # set to '1' for GPIOs 13, 19, 41, 45 or 53


class INITIALS:
    LED12_ON = True                             # 12V strip enabled
    LED5_ON = True                              # 5V WS281B strip enabled
    LED_BRIGHTNESS = 255                        # LED strips brightness
    LED_RED = 255                               # red channel brightness
    LED_GREEN = 255                             # green channel brightness
    LED_BLUE = 255                              # blue channel brightness
    LED_STRIP_DIRECTION = 1                     # WS281B strip direction, 1 for forward, -1 for backward
    LED_STRIP_DISPLAY = LEDStrip.LED_COUNT      # number of WS281B strip lit counted from current direction start
    FADE_AWAY_SPEED = 10                        # LED's fading speed


class AUDIO:
    DEFAULT_DEVICE = 1
    NO_CHANNELS = 1
    SAMPLE_RATE = 44100
    CHUNK = 768
    SENSITIVENESS = [1.25, 1.25, 1.23, 1.15, 1.15, 1.15, 1.15, 1.15, 1.15, 1.15, 1.15]
    FREQUENCIES = [0, 32, 64, 125, 250, 500, 1000, 2000, 4000, 8000, 16000, 20000]
    WEIGHTING = [2, 2, 4, 4, 8, 12, 16, 16, 32, 32]

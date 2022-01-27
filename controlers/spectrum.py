import time
from typing import Dict, Any

from initials.constants import AUDIO
import threading
import pyaudio
import random
from struct import unpack
import numpy as np
from controlers.led_control import LED


class Spec:
    def __init__(self, led: LED, device=AUDIO.DEFAULT_DEVICE):
        self._led = led
        self._device = device
        self.matrix = np.zeros(10)
        self.weighting = AUDIO.WEIGHTING
        self.frequencies = AUDIO.FREQUENCIES
        self.sensitivity = np.array(AUDIO.SENSITIVENESS)
        self._spec_thread = threading.Thread()
        self._exit_event = threading.Event()
        self._auto_thread = threading.Thread()
        self._auto_exit_event = threading.Event()
        self._fading_thread = threading.Thread()
        self._fading_exit_event = threading.Event()
        self._inertia = 0.2
        self._analyzed_frequency = 1
        self._fade_speed = 15
        self._sensitivity = 150
        self._time0 = time.time()
        random.seed()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=AUDIO.NO_CHANNELS,
                                  rate=AUDIO.SAMPLE_RATE,
                                  input=True,
                                  frames_per_buffer=AUDIO.CHUNK,
                                  input_device_index=self._device)

    def list_devices(self) -> None:
        i = 0
        n = self.p.get_device_count()
        while i < n:
            dev = self.p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                print(f"{i}. {dev['name']}")
            i += 1

    @staticmethod
    def _piff(val) -> int:
        return int(2 * AUDIO.CHUNK * val / AUDIO.SAMPLE_RATE)

    def _calculate_levels(self, data: bytes) -> None:
        matrix = np.zeros(10)
        data = unpack("%dh" % (len(data) / 2), data)
        data = np.array(data, dtype='h')
        fourier = np.fft.rfft(data)
        fourier = np.delete(fourier, len(fourier) - 1)
        power = np.abs(fourier)
        for i in range(10):
            matrix[i] = (int(np.max(power[self._piff(self.frequencies[i]): self._piff(self.frequencies[i+1]): 1]))
                         / 10) ** self.sensitivity[i+1]
        matrix = np.divide(np.multiply(matrix, self.weighting), 10_000_000 / (self.sensitivity[0] * 40)).astype(int)
        self.matrix = matrix.clip(0, 255)

    def _catch_bit(self) -> None:
        data = self.stream.read(AUDIO.CHUNK, exception_on_overflow=False)
        self._calculate_levels(data)

    def _start_monitoring(self) -> None:
        while not self._exit_event.is_set():
            self._catch_bit()
            self.spec_matrix = self.matrix

    def _start_auto(self) -> None:
        while not self._auto_exit_event.is_set():
            self._catch_bit()
            level = self.matrix[self._analyzed_frequency]
            time.sleep(0.05)

            if level > self._sensitivity:
                time_1 = time.time()
                if time_1 - self._time0 > self._inertia:
                    self._time0 = time.time()
                    if self._fading_thread.is_alive():
                        self._fading_exit_event.set()
                        self._fading_thread.join()
                    self._fading_thread = threading.Thread(target=self._fade_away)
                    self._fading_exit_event.clear()
                    self._fading_thread.start()

    def _fade_away(self) -> None:
        brightness = 255
        colors = self._led.random_colors()
        self._led.set_color(colors)
        self._led.set_brightness(brightness)
        time.sleep(0.1)
        while brightness > 0:
            if self._fading_exit_event.is_set():
                return
            self._led.set_brightness(brightness)
            brightness -= self._fade_speed
        self._led.set_brightness(0)

    def start_monitoring(self) -> None:
        self._exit_event.clear()
        self._spec_thread = threading.Thread(target=self._start_monitoring)
        self._spec_thread.start()

    def stop_monitoring(self) -> None:
        self._exit_event.set()
        self._spec_thread.join()

    def start_auto(self) -> None:
        if self._auto_thread.is_alive():
            self._auto_exit_event.set()
            self._auto_thread.join()
        self._auto_exit_event.clear()
        self._auto_thread = threading.Thread(target=self._start_auto)
        self._auto_thread.start()

    def stop_auto(self) -> None:
        self._auto_exit_event.set()
        if self._auto_thread.is_alive():
            self._auto_thread.join()

    def set_properties(self, properties: Dict[str, int]):
        """
        :param properties: accepted keys: sensitivity, inertia, frequency, fade_speed
        :return: None
        """
        if properties.keys().__contains__('sensitivity'):
            self._sensitivity = properties['sensitivity']
        if properties.keys().__contains__('inertia'):
            self._inertia = properties['inertia']
        if properties.keys().__contains__('frequency'):
            self._analyzed_frequency = properties['frequency']
        if properties.keys().__contains__('fade_speed'):
            self._fade_speed = properties['fade_speed']

    def get_properties(self) -> Dict[str, Any]:
        keys = ['autoLED', 'sensitivity', 'inertia', 'frequency', 'fade_speed']
        values = [self._auto_thread.is_alive(),
                  self._sensitivity,
                  self._inertia,
                  self._analyzed_frequency,
                  self._fade_speed]
        return dict(zip(keys, values))

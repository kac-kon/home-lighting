import time

from controlers.distance_sensor import DistanceSensor
from controlers.light_sensor import LightSensor
from controlers.monitoring import Monitoring
from controlers.motion_sensor import MotionSensor
# from controlers.orchestrator import Orchestrator
from initials.constants import INITIALS


class Sensors:
    def __init__(self,
                 orchestrator,
                 distance_sensor: DistanceSensor,
                 light_sensor: LightSensor,
                 motion_sensor: MotionSensor):
        self._orchestrator = orchestrator
        self._distance_sensor = distance_sensor
        self._light_sensor = light_sensor
        self._motion_sensor = motion_sensor

        self._motion_timeout = INITIALS.MOTION_TIMEOUT

        self._movement_monitoring = Monitoring(self._wait_for_no_motion)

        self._motion_sensor.register_motion_callback(self._motion_observer)

        self._distance_sensor.register_distance_observer(self._distance_observer)

        self._light_sensor.register_lighting_observer(self._luminosity_observer)

    def _wait_for_no_motion(self):
        count = 0
        while not self._movement_monitoring.is_event_set():
            count += 1
            time.sleep(.5)
            if count >= self._motion_timeout:
                break
        if count >= self._motion_timeout:
            self._orchestrator.lights_down()

    def _luminosity_observer(self) -> None:
        if self._light_sensor.lights_on and self._motion_sensor.is_monitored():
            self._motion_sensor.stop_monitoring()
        elif not self._light_sensor.lights_on and not self._motion_sensor.is_monitored():
            self._motion_sensor.start_monitoring()

    def _motion_observer(self) -> None:
        print('motion detected')
        if not self._orchestrator.lights_on and not self._movement_monitoring.is_thread_alive():
            self._orchestrator.lights_up()
        if self._movement_monitoring.is_thread_alive():
            self._movement_monitoring.stop_monitoring()
        self._movement_monitoring.start_monitoring()

    def _distance_observer(self) -> None:
        dist = self._distance_sensor.distance
        print(f'distance changed to: {dist}')
        if 5 <= dist <= 10:
            self._orchestrator.switch_leds()
        elif 15 <= dist <= 25:
            self._orchestrator.set_colors([255, 0, 0])
        elif 25 < dist <= 32:
            self._orchestrator.set_colors([0, 255, 0])
        elif 32 < dist <= 40:
            self._orchestrator.set_colors([0, 0, 255])
        elif 40 < dist <= 48:
            self._orchestrator.set_colors([255, 255, 255])

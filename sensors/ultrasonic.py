import sys

from sensors.base import Sensor
import RPi.GPIO as GPIO

import time

SOUND_METERS_PER_NANOSEC = 3.4 * 10 ** -7
ACCURACY_METERS = 0.1
SLEEP_QUANTUM = 0.1 / SOUND_METERS_PER_NANOSEC
MAX_RANGE_METERS = 3.8  # It is 4 but be safe
MAX_WAIT = MAX_RANGE_METERS / SOUND_METERS_PER_NANOSEC


class Ultrasonic(Sensor):
    def __init__(self, trig, echo):
        self._trig = trig
        self._echo = echo

        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

        GPIO.output(trig, False)

    def poll_measure(self):
        """TODO: Send pulse and wait for response with timeout"""
        GPIO.output(self._trig, True)
        time.sleep(0.00001)
        GPIO.output(self._echo, False)

        pulse_start = time.time()

        had_feedback = False

        while (time.time() - pulse_start) < MAX_WAIT:
            if GPIO.input(self._echo) == 0:
                had_feedback = True
                break
            time.sleep(SLEEP_QUANTUM)

        if not had_feedback:
            self._measure_lock.acquire()
            self._values = (sys.float_info.max)
            self._measure_lock.release()
            print('Ultrasonic exceeded max wait time')
            return

        pulse_duration = time.time() - pulse_start

        distance_m = pulse_duration * SOUND_METERS_PER_NANOSEC / 2.0

        self._measure_lock.acquire()
        self._values = (distance_m)
        self._measure_lock.release()
        print(f'Ultrasonic measured: {distance_m} m')

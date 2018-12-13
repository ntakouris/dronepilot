import threading

from sensors.barometer import Barometer
from sensors.gps import GPS
from sensors.imu import IMU
from sensors.ultrasonic import Ultrasonic
import board

import RPi.GPIO as GPIO

import time

'''Production configuration -- for bench testing look at poll.py'''
"""TODO: Finish wiring"""

'''Same I2C Bus for IMU and Barometer'''
IMU_SCL = board.SCL
IMU_SDA = board.SDA
IMU_ADDR = 0x68  # 0x68 | 0x69

BAROMETER_SCL = IMU_SCL
BAROMETER_SDA = IMU_SDA
BAROMETER_SEA_LEVEL_PRESSURE = 1013.25  # hPa
BAROMETER_ADDR = 0x76  # 0x76 | 0x77

ULTRASONIC_TRIG = GPIO.GPIO19
ULTRASONIC_ECHO = GPIO.GPIO26

I2C_LOCK = threading.Lock()

GPS_SERIAL = '/dev/ttyACM0'
GPS_RATE = 9600

MAGNETIC_FIELD_OFFSET = (0, 0, 0)


def init_gpio():
    GPIO.setmode(GPIO.BOARD)


def get_imu():
    return IMU(IMU_ADDR, IMU_SCL, IMU_SDA, I2C_LOCK)


def get_barometer():
    return Barometer(BAROMETER_ADDR, BAROMETER_SCL, BAROMETER_SDA, I2C_LOCK, BAROMETER_SEA_LEVEL_PRESSURE)


def get_gps():
    return GPS(GPS_SERIAL, GPS_RATE)


def get_ultrasonic():
    return Ultrasonic(ULTRASONIC_TRIG, ULTRASONIC_ECHO)


def get_sensors():
    print('Initializing sensors...')

    print(' -> IMU')

    imu = get_imu()

    print(' -> Barometer')

    barometer = get_barometer()

    print(' -> Ultrasonic')

    ultrasonic = get_ultrasonic()

    print(' -> GPS')

    gps = get_gps()

    print(' -> Sensor initialization complete')

    return [imu, barometer, ultrasonic, gps]

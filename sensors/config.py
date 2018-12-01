import threading

from sensors.barometer import Barometer
from sensors.gps import GPS
from sensors.imu import IMU
from sensors.ultrasonic import Ultrasonic
import board

'''Production configuration -- for bench testing look at poll.py'''
"""TODO: Finish wiring"""

'''Same I2C Bus for IMU and Barometer'''
IMU_SCL = board.SCL
IMU_SDA = board.SDA

BAROMETER_SCL = IMU_SCL
BAROMETER_SDA = IMU_SDA
BAROMETER_SEA_LEVEL_PRESSURE = 1013.25  # hPa

ULTRASONIC_TRIG = 0
ULTRASONIC_ECHO = 0

I2C_LOCK = threading.Lock()


def get_imu():
    return IMU(IMU_SCL, IMU_SDA, I2C_LOCK)


def get_barometer():
    return Barometer(BAROMETER_SCL, BAROMETER_SDA, I2C_LOCK, BAROMETER_SEA_LEVEL_PRESSURE)


def get_gps():
    return GPS()


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

import serial

from sensors.accelerometer import Accelerometer

'''Production configuration -- for bench testing look at monitor.py'''
def get_accelelerometer():
    return Accelerometer(serial.Serial('/dev/ttyS1', 19200, 1))


def get_gps():
    return "todo"


def get_ultrasonic():
    return "todo"


def get_barometer():
    return "todo"
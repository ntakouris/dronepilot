from sensors.base import Sensor


class IMU(Sensor):

    def __init__(self, addr, scl, sda, i2c_lock):

        self._i2c_lock = i2c_lock

    def poll_measure(self):
        """TODO: Add I2C Communication with some timeout"""
        self._i2c_lock.acquire()

        self._i2c_lock.release()

        self._measure_lock.acquire()

        self._measure_lock.release()

    def read_values(self):
        self._measure_lock.acquire()
        ret = self._values.copy()
        self._measure_lock.release()
        return ret

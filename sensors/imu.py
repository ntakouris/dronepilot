from sensors.base import Sensor


class IMU(Sensor):

    def __init__(self, scl, sda, i2c_lock):
        self.scl = scl
        self.sda = sda
        self.i2c_lock = i2c_lock

    def poll_measure(self):
        """TODO: Add I2C Communication with some timeout"""
        self.i2c_lock.acquire()

        self.i2c_lock.release()

        self.measure_lock.acquire()

        self.measure_lock.release()

    def read_values(self):
        self.measure_lock.acquire()
        ret = self.values.copy()
        self.measure_lock.release()
        return ret

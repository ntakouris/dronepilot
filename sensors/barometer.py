from sensors.base import Sensor


class Barometer(Sensor):

    def __init__(self, scl, sda):
        self.scl = scl
        self.sda = sda

    def poll_measure(self):
        """TODO: Add I2C Communication with some timeout"""
        self.measure_lock.acquire()

        self.measure_lock.release()

    def read_values(self):
        self.measure_lock.acquire()
        ret = self.values.copy()
        self.measure_lock.release()
        return ret

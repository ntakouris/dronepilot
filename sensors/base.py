from threading import Lock
from copy import deepcopy


class Sensor:
    measure_lock = Lock()
    values = ()

    def get_delay_between_measurements(self):
        return 0

    def poll_measure(self):
        return

    def dispose(self):
        return

    def read_values(self):
        self.measure_lock.acquire()
        ret = deepcopy(self.values)
        self.measure_lock.release()
        return ret

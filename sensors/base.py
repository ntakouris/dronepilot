from threading import Lock
from copy import deepcopy


class Sensor:
    _measure_lock = Lock()
    _values = ()

    def get_delay_between_measurements(self):
        return 0

    def poll_measure(self):
        return

    def dispose(self):
        return

    def read_values(self):
        self._measure_lock.acquire()
        ret = deepcopy(self._values)
        self._measure_lock.release()
        return ret

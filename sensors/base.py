from threading import Lock


class Sensor:
    measure_lock = Lock()
    values = {}

    def get_delay_between_measurements(self):
        return 0

    def poll_measure(self):
        return

    def dispose(self):
        return

    def read_values(self):
        return

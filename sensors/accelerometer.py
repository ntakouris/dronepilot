from threading import Lock


class Accelerometer:
    measure_lock = Lock()
    values = {0,0,0}

    def __init__(self, serial):
        self.serial = serial
        serial.open()

    def poll_measure(self):
        s = self.serial.read(100)
        print(f"Accelerometer raw measure: {s}.")

        self.measure_lock.acquire()

        self.measure_lock.release()

    def dispose(self):
        self.serial.close()

    def read_values(self):
        self.measure_lock.acquire()
        ret = self.values.copy()
        self.measure_lock.release()
        return ret

    @staticmethod
    def get_delay_between_measurements():
        return 2

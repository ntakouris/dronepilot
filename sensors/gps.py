from sensors.base import Sensor


class GPS(Sensor):

    """TODO: Figure out SPI wiring params"""
    def __init__(self):
        return

    def poll_measure(self):
        print(f"Gps raw measure: .")

        self.measure_lock.acquire()

        self.measure_lock.release()

    def read_values(self):
        self.measure_lock.acquire()
        ret = self.values.copy()
        self.measure_lock.release()
        return ret

    def get_delay_between_measurements(self):
        """TODO: Calculate based on baud rate"""
        return 2

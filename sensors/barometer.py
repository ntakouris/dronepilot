from sensors.base import Sensor
import busio
import adafruit_bmp280


class Barometer(Sensor):

    def __init__(self, scl, sda, i2c_lock, sea_level_pressure):
        self.scl = scl
        self.sda = sda
        self.i2c_lock = i2c_lock
        i2c = busio.I2C(scl, sda)
        self._sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        self._sensor.sea_level_pressure = sea_level_pressure

    def poll_measure(self):
        self.i2c_lock.acquire()
        val = (self._sensor.altitude)
        self.i2c_lock.release()

        self.measure_lock.acquire()
        self.values = val
        self.measure_lock.release()
        print(f'Altitude measured: {val}')


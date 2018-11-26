import serial
import time
from sensors.accelerometer import Accelerometer


def main():
    print('Initialize sensors...')
    accelerometer = Accelerometer(serial.Serial('/dev/ttyS1', 19200, 1))

    sensors = [accelerometer]

    print('Press any key to cancel measurement loop')

    time.sleep(2)

    try:
        while True:
            print('============================')
            for sensor in sensors:
                print(f'Polling {type(sensor).__name__}')
                sensor.poll_measure()
                print(f'Ended at: {time.time()}')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
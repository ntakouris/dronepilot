from sensors.config import *
import time


def poll_all_values_test():
    sensors = get_sensors()

    print('Press any key to cancel poll all values measurement loop')

    time.sleep(2)

    try:
        while True:
            print('============================')
            for sensor in sensors:
                print(f'Polling {type(sensor).__name__}')
                sensor.poll_measure()
                print(f'Ended at: {time.time()}')
    except KeyboardInterrupt:
        [s.dispose() for s in sensors]
        pass


if __name__ == '__main__':
    poll_all_values_test()

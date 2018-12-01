from threading import Thread

from sensors.config import *
import time
import sys

def test_poll_all_values():
    sensors = get_sensors()

    print('Press any key to cancel poll all values measurement loop')

    time.sleep(2)

    try:
        while True:
            print('============================')

            start = time.time()
            for sensor in sensors:
                print(f'Polling {type(sensor).__name__}')

                _start = time.time()
                sensor.poll_measure()
                _end = time.time()

                print(f'Poll time {(_start - _end) / 1000} ms')
            end = time.time()

            print(f'All sensor poll loop time {(start - end) / 1000} ms')

            time.sleep(2)
    except KeyboardInterrupt:
        [s.dispose() for s in sensors]
        pass


def test_poll_sequential_smart():
    def measure_listener(_measure_event, _kill_event):
        _now = time.time()
        while not _kill_event.is_set():
            if not _measure_event.wait(1):
                _measure_event.clear()
                print(f'All sensors measured after: {(time.time() - _now) / 1000} ms')
                _now = time.time()

    sensors = get_sensors()

    print('Press any key to cancel poll sequential smart values measurement loop')

    time.sleep(2)

    kill_event = threading.Event()
    measure_event = threading.Event()

    poller = Thread(target=test_poll_sequential_smart, args=(sensors, measure_event, kill_event))
    listener = Thread(target=measure_listener, args=(measure_event, kill_event))

    try:
        poller.start()
        listener.start()

        while True:
            """"Busy wait"""
            time.sleep(0.3)
    except KeyboardInterrupt:
        print('Setting kill event')
        kill_event.set()
        print('Joining threads')
        poller.join()
        listener.join()

        [s.dispose() for s in sensors]
        pass


def test_poll_parallel():
    return

def test_poll(sensor):
    print('Press any key to cancel barometer poll measurement loop')

    time.sleep(2)

    try:
        while True:
            start = time.time()
            sensor.poll_measure()
            print(f'{type(sensor).__name__} poll took {(time.time() - start)} ms')
    except KeyboardInterrupt:
        sensor.dispose()
        pass


def test_poll_barometer():
    test_poll(get_barometer())


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        arg = sys.argv[2]

        if arg == 'baro' or arg == 'barometer':
            test_poll(get_barometer())
        elif arg == 'gps':
            test_poll(get_gps())
        elif arg == 'imu':
            test_poll(get_imu())
        elif arg == 'ultra' or arg == 'ultrasonic':
            test_poll(get_ultrasonic())
        elif arg == 'seq-smart' or 'sequential-smart':
            test_poll_sequential_smart()
        elif arg == 'par' or 'parallel':
            test_poll_parallel()
        elif arg == 'all' or arg == '*':
            test_poll_all_values()
        else:
            print(f'Unknown test target: {arg}')
    test_poll_all_values()

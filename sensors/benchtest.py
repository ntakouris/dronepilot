from threading import Thread

from sensors.config import *
import time


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


if __name__ == '__main__':
    test_poll_all_values()

import threading
from threading import Thread

import time

''' Poll serially sensor list ordered ascending by their measurement delay'''


def poll_sequential_smart(sensors, measure_tick_event, kill_event):
    sensors.sort(key=lambda e: e.get_delay_between_measurements)

    measure_time_map = {}

    now = time.time()

    for sensor in sensors:
        measure_time_map[sensor] = now - sensor.get_delay_between_measurements()

    while not kill_event.is_set():
        start = time.time()
        for sensor in sensors:
            now = time.time()
            last_measure = measure_time_map[sensor]
            diff = now - last_measure

            print(f'Polling {type(sensor).__name__}')

            if diff < sensor.get_delay_between_measurements():
                _del = sensor.get_delay_between_measurements() - diff
                print(f'Sleeping for extra {_del / 1000} ms')
                time.sleep(_del / 1000)

            sensor.poll_measure()
            print(f'Poll ended')
        print(f'Finished polling after {(time.time() - start) / 1000} ms')
        measure_tick_event.set()


'''Poll all sensors in different threads, in parallel'''


def poll_parallel(sensors, measure_tick_event, kill_event):
    def _poll(_sensor, completed_event):
        while not kill_event.is_set():
            print(f'Polling {type(sensor).__name__}')
            _start = time.time()
            _sensor.poll_measure()
            print(f'Finished polling {type(sensor).__name__} after {(time.time() - _start) / 1000} ms')
            _start = time.time()

            completed_event.set()
            time.sleep(_sensor.get_delay_between_measurements() / 1000)

    time_wait_quantum = min(sensors, lambda s: s.get_delay_between_measurements())

    threads = []
    events = []

    for sensor in sensors:
        e = threading.Event()
        t = Thread(target=_poll, args=(sensor, e))
        events.append(e)
        threads.append(t)

    now = time.time()
    for thread in threads:
        thread.start()

    def _set_and_clear(event):
        event.wait()
        event.clear()

    while not kill_event.is_set():
        time.sleep(time_wait_quantum)
        [_set_and_clear(e) for e in events]
        print(f'Parallel poll ended after: {(time.time() - now) / 1000} ms')
        now = time.time()
        measure_tick_event.set()

    [t.join() for t in threads]


''' Poll in a for loop'''


def poll_sequential_dumb(sensors, measure_tick_event, kill_event):
    while not kill_event.is_set():
        start = time.time()
        for sensor in sensors:
            print(f'Polling {type(sensor).__name__}')
            _start = time.time()
            sensor.poll_measure()
            print(f'Poll ended after: {(time.time() - start) / 1000} ms')
        measure_tick_event.set()
        print(f'Polled all sensors after {(time.time() - start) / 1000} ms')
        start = time.time()


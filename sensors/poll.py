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
        for sensor in sensors:
            now = time.time()
            last_measure = measure_time_map[sensor]
            diff = now - last_measure

            if diff < sensor.get_delay_between_measurements():
                time.sleep(sensor.get_delay_between_measurements() - diff)

            print(f'Polling {type(sensor).__name__}')
            sensor.poll_measure()
            print(f'Poll ended at: {time.time()}')
        measure_tick_event.set()


'''Poll all sensors in different threads, in parallel'''


def poll_parallel(sensors, measure_tick_event, kill_event):
    def _poll(_sensor, completed_event):
        while not kill_event.is_set():
            _sensor.poll_measure()
            completed_event.set()
            time.sleep(_sensor.get_delay_between_measurements())

    time_wait_quantum = min(sensors, lambda s: s.get_delay_between_measurements())

    threads = []
    events = []

    for sensor in sensors:
        e = threading.Event()
        t = Thread(target=_poll, args=(sensor, e))
        events.append(e)
        threads.append(t)

    for thread in threads:
        thread.start()

    def _set_and_clear(event):
        event.wait()
        event.clear()

    while not kill_event.is_set():
        time.sleep(time_wait_quantum)
        [_set_and_clear(e) for e in events]
        print(f'Parallel poll ended at: {time.time()}')
        measure_tick_event.set()

    [t.join() for t in threads]


''' Poll in a for loop'''


def poll_sequential_dumb(sensors, measure_tick_event, kill_event):
    while not kill_event.is_set():
        for sensor in sensors:
            print(f'Polling {type(sensor).__name__}')
            sensor.poll_measure()
            print(f'Poll ended at: {time.time()}')
        measure_tick_event.set()


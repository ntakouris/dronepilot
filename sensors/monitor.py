import threading
from threading import Thread

import serial
import time

from sensors.accelerometer import Accelerometer

''' Poll serially sensor list ordered ascending by their measurement delay'''


def serial_poll(sensors, measure_tick_event, kill_event):
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


def parallel_poll(sensors, measure_tick_event, kill_event):
    def _poll(sensor, completed_event):
        while not kill_event.is_set():
            sensor.poll_measure()
            completed_event.set()
            time.sleep(sensor.get_delay_between_measurements())

    time_wait_quantum = min(sensors, lambda s: s.get_delay_between_measurements())

    threads = []
    events = []

    for sensor in sensors:
        e = threading.Event()
        t = Thread(target=_poll(sensor, e))
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
        for sensor in sensors:
            sensor.dispose()
        pass


if __name__ == '__main__':
    main()

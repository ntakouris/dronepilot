from threading import Lock, Thread

from sensors.barometer import Barometer
from sensors.gps import GPS
from sensors.imu import IMU


def start(predict_event, update_event, new_state_event, kill_event):
    event_lock = Lock()

    thread_update = Thread(target=_update, args=(update_event, new_state_event, kill_event, event_lock))
    thread_predict = Thread(target=_predict, args=(predict_event, new_state_event, kill_event, event_lock))

    thread_update.start()
    thread_predict.start()


pos = (0, 0)  # (lat, lng)
w_accel = ()  #
w_rot = ()  #

l_accel = ()  # (x, y, z)
l_rot = ()  # (x, y, z)

ori = ()  #

height = 0

_first_predict = True
_has_updated_at_least_once = True


def _update(update_event, new_state_event, kill_event, event_lock):
    global pos, _has_updated_at_least_once

    while not kill_event.is_set():
        if update_event.wait(1):
            event_lock.acquire()
            _has_updated_at_least_once = True

            (lat, lng) = update_event.values[type(GPS).__name__]
            print(f'Updating state with (lat: {lat}, lng: {lng})')

            pos = (lat, lng)

            update_event.unset()

            new_state_event.values = _state_copy()
            new_state_event.set()
            event_lock.release()


def _predict(predict_event, new_state_event, kill_event, event_lock):
    global _first_predict, _has_updated_at_least_once
    global pos, w_accel, w_rot, l_accel, l_rot, ori, height

    while not kill_event.is_set():
        if predict_event.wait(1):
            event_lock.acquire()

            ((ax, ay, az), (rx, ry, rz), (ox, oy, oz)) = predict_event.values[type(IMU).__name__]

            (height_from_sealevel) = predict_event.values[type(Barometer).__name__]

            l_accel = (ax, ay, az)
            l_rot = (rx, ry, rz)
            ori = (ox, oy, oz)

            if _first_predict or not _has_updated_at_least_once:
                _first_predict = False
                predict_event.unset()
                event_lock.release()
                continue

            """TODO: Kalman & complementary filter goes here"""

            print(f'Updating state with (height: {height_from_sealevel})')
            height = height_from_sealevel

            predict_event.unset()
            new_state_event.values = _state_copy()
            new_state_event.set()
            event_lock.release()


def _state_copy():
    global pos, height, w_accel, w_rot, ori

    return (pos, height, w_accel, w_rot, ori)

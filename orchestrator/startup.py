import threading

from comms import betaflight
from sensors.config import get_gps
from sensors.poll import poll_parallel, poll_sequential_smart
import estimations.engine
import goals.listener


def main():
    kill_event = threading.Event()
    predict_event = threading.Event()
    update_event = threading.Event()
    new_state_event = threading.Event()
    new_tpyr_event = threading.Event()  # Throttle Pitch Yaw Roll

    sensor_list = []

    gps = get_gps()

    gps.wait_for_satellite()

    print('Initializing pollers')
    poll_parallel(sensor_list, predict_event, kill_event)
    poll_sequential_smart([gps], update_event, kill_event)

    print('Initializing estimation engine')
    estimations.engine.start(predict_event, update_event, new_state_event, kill_event)

    print('Initializing goal checker')
    goals.listener.start(new_state_event, new_tpyr_event, kill_event)

    print('Initializing betaflight comms')
    betaflight.start(new_tpyr_event, kill_event)


if __name__ == '__main__':
    main()

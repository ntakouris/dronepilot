import threading

from comms import betaflight
from estimations.util import get_pressure_at_sea_level, get_magnetic_field_offset
import sensors.config
from sensors.poll import poll_parallel, poll_sequential_smart
import estimations.engine
import goals.listener


def main():
    kill_event = threading.Event()
    predict_event = threading.Event()
    update_event = threading.Event()
    new_state_event = threading.Event()
    new_tpyr_event = threading.Event()  # Throttle Pitch Yaw Roll

    gps = sensors.config.get_gps()

    (lat, lng) = gps.wait_for_satellite()

    sensors.config.BAROMETER_SEA_LEVEL_PRESSURE = get_pressure_at_sea_level(lat, lng)
    sensors.config.MAGNETIC_FIELD_OFFSET = get_magnetic_field_offset(lat, lng)

    sensor_list = [sensors.config.get_imu(), sensors.config.get_barometer()]

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

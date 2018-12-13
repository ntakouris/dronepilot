from threading import Thread


def start(new_state_event, new_tpyr_event, kill_event):
    Thread(target=_listen, args=(new_state_event, new_tpyr_event, kill_event)).start()


def _listen(new_state_event, new_tpyr_event, kill_event):
    while not kill_event.is_set():
        if new_state_event.wait(1):
            new_state_event.unset()
            """TODO: Calculations go here"""
            new_tpyr_event.set()

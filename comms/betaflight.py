from threading import Thread


def start(new_tpyr_event, kill_event):
    Thread(target=_command, args=(new_tpyr_event, kill_event)).start()


def _command(new_tpyr_event, kill_event):
    while not kill_event.is_set():
        if new_tpyr_event.wait(1):
            new_tpyr_event.unset()

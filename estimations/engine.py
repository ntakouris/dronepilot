from threading import Lock, Thread


def start(predict_event, update_event, new_state_event, kill_event):
    event_lock = Lock()

    thread_update = Thread(target=_update, args=(update_event, new_state_event, kill_event, event_lock))
    thread_predict = Thread(target=_predict, args=(predict_event, new_state_event, kill_event, event_lock))

    thread_update.start()
    thread_predict.start()


def _update(update_event, new_state_event, kill_event, event_lock):
    while not kill_event.is_set():
        if update_event.wait(1):
            update_event.unset()
            event_lock.acquire()

            new_state_event.set()
            event_lock.release()


def _predict(predict_event, new_state_event, kill_event, event_lock):
    while not kill_event.is_set():
        if predict_event.wait(1):
            predict_event.unset()
            event_lock.acquire()

            new_state_event.set()
            event_lock.release()

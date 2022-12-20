import watchdog.events
import watchdog.observers
import time
from os import path
from datetime import datetime
from log_setup import logger


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, file_name, callback):
        logger.debug(f"starting to observe: {file_name}")
        watchdog.events.PatternMatchingEventHandler.__init__(
            self,
            patterns=[file_name],
            ignore_directories=True,
            case_sensitive=False,
        )
        self.callback = callback

    def on_modified(self, event):
        logger.debug(
            "Watchdog received modified event - % s., Time: %s"
            % (event.src_path, datetime.now().isoformat())
        )
        self.callback()


def setup_watchdog(path_to_observe, callback):
    dir, file = path.split(path_to_observe)
    event_handler = Handler(file, callback)
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

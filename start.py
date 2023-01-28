from global_configs import PLAYER_FILE_PATH, VERBOSE, PORT
from src.log_setup import logger
from src.cachorro import setup_watchdog
import threading
from src.memory_db import memory_db

from src.server_setup import setup_server

logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")
memory_db.update_stats()


def main_loop():
    memory_db.update_stats()


t1 = threading.Thread(
    target=lambda: setup_watchdog(PLAYER_FILE_PATH, main_loop), daemon=True
)
t1.start()


app, socketio = setup_server(memory_db)
main_loop()
socketio.run(app, port=PORT)

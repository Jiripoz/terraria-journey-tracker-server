from global_configs import PLAYER_FILE_PATH, VERBOSE, PORT
from src.log_setup import logger

logger.info("Starting script")
logger.info(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.info(f"VERBOSE: {VERBOSE}")

from src.cachorro import setup_watchdog
import threading
from src.memory_db import memory_db
from src.server_setup import setup_server

memory_db.update_stats()


def main_loop():
    memory_db.update_stats()


t1 = threading.Thread(target=lambda: setup_watchdog(PLAYER_FILE_PATH, main_loop), daemon=True)
t1.start()


app, socketio = setup_server(memory_db)
main_loop()
socketio.run(app, port=PORT, host='0.0.0.0')

from global_configs import PLAYER_FILE_PATH, VERBOSE, PORT
from src.log_setup import logger
from src.char import get_char
from src.cachorro import setup_watchdog
from src.recipe_db import recipe_db
from src.memory_db import MemoryDB
import threading

from src.server_setup import setup_server

logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")
memory_db = MemoryDB()


def main_loop():
    global memory_db
    player = get_char(PLAYER_FILE_PATH)
    # player.print_progress_overview()
    # player.print_partially_researched()
    # player.get_easy_researchs()
    memory_db.update_kv("player", player)


t1 = threading.Thread(
    target=lambda: setup_watchdog(PLAYER_FILE_PATH, main_loop), daemon=True
)
t1.start()


app, socketio = setup_server(memory_db)
socketio.run(app, port=PORT)

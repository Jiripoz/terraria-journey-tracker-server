from global_configs import PLAYER_FILE_PATH, VERBOSE, PORT
from src.log_setup import logger
from src.char import get_char, fetch_player
from src.cachorro import setup_watchdog
from src.recipe_db import recipe_db
import threading

from src.server_setup import setup_server

logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")
player_info, player_overview = fetch_player()


def main_loop():
    global player_info
    player_info, player_overview = fetch_player()


t1 = threading.Thread(
    target=lambda: setup_watchdog(PLAYER_FILE_PATH, main_loop), daemon=True
)
t1.start()


app, socketio = setup_server(player_info, player_overview)
main_loop()
socketio.run(app, port=PORT)

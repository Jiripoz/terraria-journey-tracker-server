from global_configs import PLAYER_FILE_PATH, VERBOSE
from src.log_setup import logger
from src.char import get_char
from src.cachorro import setup_watchdog

logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")


def main_loop():
    player = get_char(PLAYER_FILE_PATH)
    player.print_progress_overview()
    player.print_partially_researched()


main_loop()

setup_watchdog(PLAYER_FILE_PATH, main_loop)

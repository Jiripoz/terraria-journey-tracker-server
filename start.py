from global_configs import PLAYER_FILE_PATH, VERBOSE
from log_setup import logger
from src.char import get_char

logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")

a = get_char()
print(a.items_progress)

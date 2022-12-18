from global_configs import PLAYER_FILE_PATH, VERBOSE
from log_setup import logger
from src.item_db import item_db

logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")

# Example usage:
item_1 = item_db.get_item(1)
logger.info(item_1)

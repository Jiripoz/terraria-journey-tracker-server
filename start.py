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


# from flask import Flask, render_template
# from flask_socketio import SocketIO
# from flask_cors import CORS

# app = Flask(__name__, instance_relative_config=True)
# app.config.update(SECRET_KEY="a")

# print("Starting with config:")
# print(app.config)

# CORS(app)
# app.config["CORS_HEADER"] = "Content-Type"

# socketio = SocketIO(app, cors_allowed_origins="*", logger=True)


# if __name__ == "__main__":
#     socketio.run(app)

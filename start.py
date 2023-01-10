from global_configs import PLAYER_FILE_PATH, VERBOSE, PORT
from src.log_setup import logger
from src.char import get_char
from src.cachorro import setup_watchdog
from src.recipe_db import recipe_db
import threading
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS


logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")
last_player = None


def main_loop():
    global last_player
    player = get_char(PLAYER_FILE_PATH)
    # player.print_progress_overview()
    # player.print_partially_researched()
    # player.get_easy_researchs()
    last_player = player


t1 = threading.Thread(
    target=lambda: setup_watchdog(PLAYER_FILE_PATH, main_loop), daemon=True
)
t1.start()

print("oi")
app = Flask(__name__, instance_relative_config=True)
app.config.update(SECRET_KEY="a")

print("Starting with config:")
print(app.config)

CORS(app)
app.config["CORS_HEADER"] = "Content-Type"


@app.route("/config")
def get_server_config():
    return jsonify(
        {
            "player_file_path": PLAYER_FILE_PATH,
        }
    )


@app.route("/player")
def get_player():
    global last_player
    if last_player == None:
        return jsonify({"leleks": "leleks"})

    return jsonify(last_player.get_progress_json())


socketio = SocketIO(app, cors_allowed_origins="*", logger=True)


socketio.run(app, port=PORT)
print("antes do start")

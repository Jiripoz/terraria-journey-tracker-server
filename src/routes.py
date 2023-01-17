from flask import jsonify
from global_configs import PLAYER_FILE_PATH
import json


def setup_routes(app, player_info):
    @app.route("/config")
    def get_server_config():
        return jsonify(
            {"player_file_path": PLAYER_FILE_PATH, "teste": player_info["partial"]}
        )

    @app.route("/player")
    def get_player():
        with open("data/display.json", "r") as f:
            display = json.load(f)
        if display == None:
            return jsonify({"leleks": "leleks"})

        return jsonify(display)

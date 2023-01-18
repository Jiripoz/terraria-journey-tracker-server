from flask import jsonify
from global_configs import PLAYER_FILE_PATH
import json


def setup_routes(app, player_info, player_overview):
    @app.route("/config")
    def get_server_config():
        return jsonify(
            {"player_file_path": PLAYER_FILE_PATH, "teste": player_info["partial"]}
        )

    @app.route("/overview")
    def get_player():
        return jsonify(player_overview)

    @app.route("/easy")
    def get_easy():
        return jsonify()

from flask import jsonify
from global_configs import PLAYER_FILE_PATH


def setup_routes(app, memory_db):
    @app.route("/config")
    def get_server_config():
        return jsonify(
            {
                "player_file_path": PLAYER_FILE_PATH,
            }
        )

    @app.route("/player")
    def get_player():
        last_player = memory_db.get_value("player")
        if last_player == None:
            return jsonify({"leleks": "leleks"})

        return jsonify(last_player.get_progress_json())

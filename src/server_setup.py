from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from src.routes import setup_routes


def setup_server(player_info, player_overview):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)
    app.config["CORS_HEADER"] = "Content-Type"

    setup_routes(app, player_info, player_overview)

    return app, SocketIO(app, cors_allowed_origins="*", logger=True)

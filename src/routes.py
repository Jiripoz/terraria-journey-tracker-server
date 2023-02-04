from flask import jsonify
from global_configs import PLAYER_FILE_PATH
import json
from src.memory_db import memory_db


def setup_routes(app, memory_db):
    @app.route("/config")
    def get_server_config():
        return jsonify({"player_file_path": PLAYER_FILE_PATH})

    @app.route("/overview")
    def get_overview():
        return jsonify(memory_db.overview)

    @app.route("/items")
    def get_items():
        return jsonify(memory_db.items)

    @app.route("/items-progress")
    def get_researched():
        return jsonify(memory_db.items_progress)

    # @app.route("/items")
    # def get_item():
    #     return memory_db.items

    # @app.route("/recipe_db")
    # def get_recipe():
    #     return memory_db.recipes

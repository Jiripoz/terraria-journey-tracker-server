from src.item_db import item_db
from src.recipe_db import recipe_db, RecipeDB
from src.char import fetch_player
import json

with open("data/stations.json", "r") as s:
    station_list = json.load(s)


class MemoryDB:
    def __init__(self) -> None:
        self.items = item_db.raw_dict
        self.recipes: RecipeDB = recipe_db
        self.overview, self.items_progress = fetch_player()
        self.stations = station_list
        # self.config: dict ver depois como pegar input do svelte

    def update_stats(self):
        self.overview, self.items_progress = fetch_player()
        return

    # def update_config(self): ver depois como pegar input do svelte
    #     return


memory_db = MemoryDB()

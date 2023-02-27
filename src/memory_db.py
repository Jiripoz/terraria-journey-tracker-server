from src.item_db import item_db
from src.recipe_db import recipes, RecipeDB
from src.char import fetch_player
from src.crafting_station_db import fetch_stations
from src.recipe_db import fetch_recipe_endpoint


class MemoryDB:
    def __init__(self) -> None:
        self.items = item_db.raw_dict
        self.recipes = fetch_recipe_endpoint()
        self.overview, self.items_progress, self.stations = fetch_player()
        # self.config: dict ver depois como pegar input do svelte

    def update_stats(self):
        self.overview, self.items_progress, self.stations = fetch_player()
        self.recipes = fetch_recipe_endpoint()
        return

    # def update_config(self): ver depois como pegar input do svelte
    #     return


memory_db = MemoryDB()

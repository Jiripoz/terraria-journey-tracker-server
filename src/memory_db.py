from src.item_db import item_db, ItemDB
from src.recipe_db import recipe_db, RecipeDB
from src.char import fetch_player


class MemoryDB:
    def __init__(self) -> None:
        self.items: ItemDB = item_db
        self.recipes: RecipeDB = recipe_db
        self.partial, self.overview, self.easy = fetch_player()
        # self.config: dict ver depois como pegar input do svelte

    def update_stats(self):
        self.partial, self.overview, self.easy = fetch_player()
        return

    # def update_config(self): ver depois como pegar input do svelte
    #     return


memory_db = MemoryDB()

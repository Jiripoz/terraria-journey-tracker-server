from src.item_db import item_db
import json
import os
from os import path
from dataclasses import dataclass
import re

RECIPE_JSON_PATH = str(path.join(path.abspath(os.getcwd()), "data", "recipe.json"))


@dataclass
class Recipe:
    id: int
    name: str
    station: str
    ingredients: dict

    def __str__(self):
        return f"item name: {self.name}, id: {self.id}, station: {self.station}"


def get_ingredients(r):
    lst = [x for x in re.split("[Â|^|¦]", r["args"]) if x != ""]
    ing_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return ing_dct


class RecipeDB:
    def __init__(self, recipes: list):
        self.recipes_list = {}

        for recipe in recipes:
            self.recipes_list[recipe["id"]] = Recipe(
                id=recipe["id"],
                name=recipe["name"],
                station=recipe["station"],
                ingredients=recipe["ingredients"],
            )

    def get_recipe(self, item_id: int):
        if item_id in self.recipes_list:
            return self.recipes_list[item_id]


with open(RECIPE_JSON_PATH) as f:
    recipes = json.load(f)
    recipe_db = RecipeDB(recipes=recipes)

print(recipe_db.get_recipe(10))

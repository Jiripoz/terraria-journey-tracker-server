from src.item_db import item_db
import json
import os
from os import path
from dataclasses import dataclass
import re

RECIPE_JSON_PATH = str(path.join(path.abspath(os.getcwd()), "data", "recipe.json"))


@dataclass
class Recipe:
    result: str
    resultid: int
    station: str
    ingredients: dict

    def __str__(self):
        return f"item name: {self.result}, id: {self.resultid}, station: {self.station}"


def get_ingredients(r):
    lst = [x for x in re.split("[Â|^|¦]", r["args"]) if x != ""]
    ing_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return ing_dct


class RecipeDB:
    def __init__(self, recipes: list):
        self.recipes_dict = {}

        for recipe in recipes:
            self.recipes_dict[recipe["resultid"]] = Recipe(
                result=recipe["result"],
                resultid=recipe["resultid"],
                station=recipe["station"],
                ingredients=get_ingredients(recipe),
            )

    def get_recipe(self, item_id: int):
        if item_id in self.recipes_dict:
            return self.recipes_dict[item_id]


with open(RECIPE_JSON_PATH) as f:
    recipes = json.load(f)
    recipe_db = RecipeDB(recipes=recipes)

# print(recipe_db.get_recipe("100"))

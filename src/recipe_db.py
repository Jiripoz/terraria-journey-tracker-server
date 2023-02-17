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


def fetch_recipe_endpoint():
    recipe_endpoint = {}
    for recipe in recipes:
        try:
            if recipe["id"] in list(recipe_endpoint):
                recipe_endpoint[int(recipe["id"])].append(
                    {
                        "id": int(recipe["id"]),
                        "name": recipe["name"],
                        "station": recipe["station"],
                        "ingredients": recipe["ingredients"],
                    }
                )
                continue
            else:
                recipe_endpoint[int(recipe["id"])] = []
                recipe_endpoint[int(recipe["id"])].append(
                    {
                        "id": int(recipe["id"]),
                        "name": recipe["name"],
                        "station": recipe["station"],
                        "ingredients": recipe["ingredients"],
                    }
                )
                continue
        except Exception as e:
            print(e, recipe["id"])
            continue
    return recipe_endpoint

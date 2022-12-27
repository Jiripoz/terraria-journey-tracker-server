import requests
import json
import re
import sys
from src.item_db import item_db
from src.log_setup import logger

logger.debug("Running fetch_recipe.py...")

API = "https://terraria.wiki.gg//api.php"
PARAMS = {
    "action": "cargoquery",
    "format": "json",
    "tables": "Recipes",
    "fields": "result, resultid, station, args",
    "offset": 0,
}

S = requests.Session()
R = S.get(url=API, params=PARAMS)
DATA = R.json()
final = []

while DATA["cargoquery"] != []:
    try:
        for item in DATA["cargoquery"]:
            final.append(item["title"])

        PARAMS["offset"] += 50
        R = S.get(url=API, params=PARAMS)
        DATA = R.json()

    except:
        break


with open("data/raw_recipe.json", "w") as f:
    json.dump(final, f, indent=4)

with open("alternative_db.json", "r") as g:
    alternative_db = json.load(g)


def get_ids(lst):
    for j in alternative_db:
        if lst == j:
            ids = []
            for item in alternative_db[j]:
                ids.append(int(item))
            return ids
    try:
        return int(item_db.get_item_by_name(str(lst)).id)
    except:
        return lst


def prepare(r):
    lst = [x for x in re.split("[Â|^|¦]", r) if x != ""]
    ingredients = []
    for i in range(0, len(lst), 2):
        name = lst[i]
        id = get_ids(lst[i])
        amount = lst[i + 1]
        ingredients.append({"name": name, "id": id, "amount": amount})
    return ingredients


ff = []
for item in final:
    try:
        entry = {
            "id": int(item["resultid"]),
            "name": item["result"],
            "station": item["station"],
            "ingredients": prepare(item["args"]),
        }
        ff.append(entry)
    except:
        entry = {
            "id": item["resultid"],
            "name": item["result"],
            "station": item["station"],
            "ingredients": prepare(item["args"]),
        }
        ff.append(entry)


with open("data/recipe.json", "w") as f:
    json.dump(ff, f, indent=4)

logger.debug("Done! Recipes saved in data folder as recipe.json and raw_recipe.json")

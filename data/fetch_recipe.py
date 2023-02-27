import requests
import json
import re
import sys
from src.item_db import item_db
from src.log_setup import logger

# logger.debug("Running fetch_recipe.py...")

# API = "https://terraria.wiki.gg//api.php"
# PARAMS = {
#     "action": "cargoquery",
#     "format": "json",
#     "tables": "Recipes",
#     "fields": "result, resultid, station, args",
#     "offset": 0,
# }

# S = requests.Session()
# R = S.get(url=API, params=PARAMS)
# DATA = R.json()
# final = []

# while DATA["cargoquery"] != []:
#     try:
#         for item in DATA["cargoquery"]:
#             final.append(item["title"])

#         PARAMS["offset"] += 50
#         R = S.get(url=API, params=PARAMS)
#         DATA = R.json()

#     except:
#         break


# with open("data/raw_recipe.json", "w") as f:
#     json.dump(final, f, indent=4)

with open("data/raw_recipe.json", "r") as f:
    final = json.load(f)


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
    lst = [x for x in re.split("[Â|^|¦]", r["args"]) if x != ""]
    ingredients = []
    for i in range(0, len(lst), 2):
        name = lst[i]
        id = get_ids(lst[i])
        amount = lst[i + 1]
        ingredients.append({"name": name, "id": id, "amount": amount})
    return ingredients


special_stations = {
    "By Hand": [0],
    "Demon Altar": [-1],
    "Honey": [-2],
    "Lava": [-3],
    "Living Wood": [-4],
    "Placed Bottle": [-5],
    "Shimmer": [-6],
    "Water": [-7],
    "Table and Chair": [-8],
    "Work Bench and Chair": [-9],
    "Bone Welder and Ecto Mist": [-10],
    "Heavy Work Bench and Ecto Mist": [-11],
    "Iron Anvil and Ecto Mist": [-12],
    "Loom and Ecto Mist": [-13],
    "Tinkerer's Workshop and Ecto Mist": [-14],
    "Work Bench and Ecto Mist": [-15],
    "Crystal Ball and Honey": [-16],
    "Crystal Ball and Lava": [-17],
    "Crystal Ball and Water": [-18],
    "Sky Mill and Snow Biome": [-19],
    "Sky Mill and Water": [-20],
}


def get_station(r):
    if r in list(special_stations):
        return special_stations[r]
    else:
        return [item_db.get_item_by_name(str(r)).id]


ff = []
for item in final:
    ingredients = prepare(item)
    try:
        station = get_station(item["station"])
    except:
        station = item["station"]

    try:
        item_id = int(item["resultid"])
    except:
        item_id = item["resultid"]

    entry = {
        "id": item_id,
        "name": item["result"],
        "station": station,
        "ingredients": ingredients,
    }
    ff.append(entry)


with open("data/recipe.json", "w") as f:
    json.dump(ff, f, indent=4)

logger.debug("Done! Recipes saved in data folder as recipe.json and raw_recipe.json")

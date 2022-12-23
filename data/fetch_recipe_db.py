import requests
import json
from collections import ChainMap

API = "https://terraria.wiki.gg//api.php"
PARAMS = {
    "action": "cargoquery",
    "format": "json",
    "tables": "Recipes",
    "fields": "result, resultid, station, ingredients, args",
    "offset": 0,
}

S = requests.Session()


R = S.get(url=API, params=PARAMS)

DATA = R.json()

final = []

while PARAMS["offset"] < 10000:
    try:
        R = S.get(url=API, params=PARAMS)
        DATA = R.json()
        if DATA["cargoquery"] == []:
            print(DATA["cargoquery"])
            break
        for item in DATA["cargoquery"]:
            final.append(item["title"])

        PARAMS["offset"] += 50

    except:
        break

with open("recipe_db.json", "w") as f:
    json.dump(final, f)

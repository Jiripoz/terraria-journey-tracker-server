import requests
import json

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

while DATA["cargoquery"] != []:
    try:
        for item in DATA["cargoquery"]:
            final.append(item["title"])

        PARAMS["offset"] += 50
        R = S.get(url=API, params=PARAMS)
        DATA = R.json()

    except:
        break

with open("recipe_db.json", "w") as f:
    json.dump(final, f)

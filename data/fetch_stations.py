import json
from src.item_db import item_db

with open("data/recipe.json", "r") as f:
    recipes = json.load(f)

special_stations = {
    0: {
        "name": "By Hand",
        "imageUrl": ["https://terraria.wiki.gg/images/8/86/Hand_Of_Creation.png"],
    },
    -1: {"name": "Demon Altar", "imageUrl": ["https://terraria.wiki.gg/images/f/f8/Demon_Altar.png"]},
    -2: {"name": "Honey", "imageUrl": ["https://terraria.wiki.gg/images/c/c6/Honey.png"]},
    -3: {
        "name": "Lava",
        "imageUrl": ["https://terraria.wiki.gg/images/9/9f/Flame.png"],
    },
    -4: {
        "name": "Living Wood",
        "imageUrl": ["https://terraria.wiki.gg/images/c/cc/Living_Wood_%28placed%29.png"],
    },
    -5: {
        "name": "Placed Bottle",
        "imageUrl": ["https://terraria.wiki.gg/images/4/40/Bottle_%28crafting_station%29.png"],
    },
    -6: {
        "name": "Shimmer",
        "imageUrl": ["https://terraria.wiki.gg/images/b/bf/Shimmer.gif"],
    },
    -7: {
        "name": "Water",
        "imageUrl": ["https://terraria.wiki.gg/images/9/9d/Water.png"],
    },
    -8: {
        "name": "Table and Chair",
        "imageUrl": ["https://terraria.wiki.gg/images/0/00/Any_Table.gif"],
    },
    -9: {
        "name": "Work Bench and Chair",
        "imageUrl": ["https://terraria.wiki.gg/images/d/d5/Any_Work_Bench.gif"],
    },
    -10: {
        "name": "Bone Welder and Ecto Mist",
        "imageUrl": ["https://terraria.wiki.gg/images/b/b3/Bone_Welder_%28placed%29.gif"],
    },
    -11: {
        "name": "Heavy Work Bench and Ecto Mist",
        "imageUrl": ["https://terraria.wiki.gg/images/1/17/Heavy_Work_Bench_%28placed%29.png"],
    },
    -12: {
        "name": "Iron Anvil and Ecto Mist",
        "imageUrl": ["https://terraria.wiki.gg/images/c/c3/Iron_Anvil.png"],
    },
    -13: {
        "name": "Loom and Ecto Mist",
        "imageUrl": ["https://terraria.wiki.gg/images/9/9d/Loom_%28placed%29.png"],
    },
    -14: {
        "name": "Tinkerer's Workshop and Ecto Mist",
        "imageUrl": ["https://terraria.wiki.gg/images/0/03/Tinkerer%27s_Workshop_%28placed%29.png"],
    },
    -15: {
        "name": "Work Bench and Ecto Mist",
        "imageUrl": ["https://terraria.wiki.gg/images/d/d5/Any_Work_Bench.gif"],
    },
    -16: {
        "name": "Crystal Ball and Honey",
        "imageUrl": ["https://terraria.wiki.gg/images/6/6f/Crystal_Ball_%28placed%29.png"],
    },
    -17: {
        "name": "Crystal Ball and Lava",
        "imageUrl": ["https://terraria.wiki.gg/images/6/6f/Crystal_Ball_%28placed%29.png"],
    },
    -18: {
        "name": "Crystal Ball and Water",
        "imageUrl": ["https://terraria.wiki.gg/images/6/6f/Crystal_Ball_%28placed%29.png"],
    },
    -19: {
        "name": "Sky Mill and Snow Biome",
        "imageUrl": ["https://terraria.wiki.gg/images/4/4c/Sky_Mill_%28placed%29.gif"],
    },
    -20: {
        "name": "Sky Mill and Water",
        "imageUrl": ["https://terraria.wiki.gg/images/4/4c/Sky_Mill_%28placed%29.gif"],
    },
}


stations_id_list = []
for recipe in recipes:
    item_stations = recipe["station"]
    if type(item_stations) != int:
        for station in item_stations:
            stations_id_list.append(station)
        continue
    else:
        stations_id_list.append(item_stations)


def get_craftables(station_id):
    craftable_list = []
    for recipe in recipes:
        if int(recipe["station"][0]) == station_id:
            if recipe["id"] in craftable_list:
                continue
            else:
                craftable_list.append(recipe["id"])

    return craftable_list


station_list = {}
for id in set(stations_id_list):
    if id in list(special_stations):
        station = special_stations[id]
        station_list[id] = {
            "id": id,
            "name": station["name"],
            "imageUrl": station["imageUrl"],
            "craftables": get_craftables(id),
        }

        continue
    else:
        station = item_db.get_item(id)
        station_list[id] = {
            "id": station.id,
            "name": station.name,
            "imageUrl": "https://terraria.wiki.gg/images/" + station.imageUrl,
            "craftables": get_craftables(station.id),
        }


with open("data/stations.json", "w") as s:
    json.dump(station_list, s, indent=4)

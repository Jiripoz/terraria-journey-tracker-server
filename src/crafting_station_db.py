import json
from src.item_db import item_db

with open("data/stations.json", "r") as s:
    station_list = json.load(s)

special_stations = [i for i in range(-20, 1)]

print(special_stations)


def check_station():
    return


def fetch_stations(easy, items_progress):
    crafting_stations = []
    print(type(crafting_stations))
    for station in station_list:
        if station["id"] in special_stations:
            crafting_stations.append(
                {
                    "id": station["id"],
                    "name": station["name"],
                    "imageUrl": station["imageUrl"],
                    "craftables": station["craftables"],
                    "research": station["research"],
                    "progress": station["progress"],
                    "easy": station["easy"],
                }
            )

            continue
        else:
            print(station["id"])
            print(item_db.get_item(int(station["id"])))
            crafting_stations.append(
                {
                    "id": station["id"],
                    "name": station["name"],
                    "imageUrl": station["imageUrl"],
                    "craftables": station["craftables"],
                    "research": item_db.get_item(station["id"]).research,
                    "progress": items_progress[station["id"]] if station["id"] in items_progress else 0,
                    "easy": station["id"] in easy,
                }
            )

    return crafting_stations

import json
from src.item_db import item_db

with open("data/stations.json", "r") as s:
    station_list = json.load(s)

special_stations = [i for i in range(-20, 1)]


def check_station():
    return


def fetch_stations():
    crafting_stations = []
    for station in station_list:
        if station["id"] in special_stations:
            crafting_stations.append(
                {
                    "id": station["id"],
                    "name": station["name"],
                    "imageUrl": station["imageUrl"],
                    "craftables": station["craftables"],
                }
            )

            continue
        else:
            crafting_stations.append(
                {
                    "id": station["id"],
                    "name": station["name"],
                    "imageUrl": station["imageUrl"],
                    "craftables": station["craftables"],
                }
            )

    return crafting_stations

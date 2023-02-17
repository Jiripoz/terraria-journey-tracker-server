import json
from src.item_db import item_db

with open("data/stations.json", "r") as s:
    station_list = json.load(s)

special_stations = [i for i in range(-20, 1)]


def check_station():
    return


def fetch_stations():
    crafting_stations = {}
    for id in station_list:
        if id in special_stations:
            crafting_stations[id] = {
                "id": station_list[id]["id"],
                "name": station_list[id]["name"],
                "imageUrl": station_list[id]["imageUrl"],
                "craftables": station_list[id]["craftables"],
            }

            continue
        else:
            crafting_stations[id] = {
                "id": station_list[id]["id"],
                "name": station_list[id]["name"],
                "imageUrl": station_list[id]["imageUrl"],
                "craftables": station_list[id]["craftables"],
            }

    return crafting_stations

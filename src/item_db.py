from dataclasses import dataclass
import json
import os
from os import path
import sys

sys.path.append("../")
IMAGE_ROOT_URL = "https://static.wikia.nocookie.net/terraria_gamepedia/images/"
WIKI_ROOT_URL = "https://terraria.fandom.com/wiki/"
ITEMS_JSON_PATH = str(path.join(path.abspath(os.getcwd()), "data", "items.json"))


@dataclass
class Item:
    id: int
    name: str
    research: int
    imageUrl: str
    internalName: str
    itemUrl: str
    category: list

    def __str__(self):
        return f"[{self.id}] {self.name} - {self.category} | Needs {self.research} for full research"


class ItemDB:
    def __init__(self, items: list):
        self.items_dict = {}
        self.raw_dict = items

        for id in items:
            self.items_dict[id] = Item(
                id=id,
                name=items[id]["name"],
                internalName=items[id]["internalName"],
                itemUrl=WIKI_ROOT_URL + items[id]["itemUrl"],
                imageUrl=items[id]["imageUrl"],
                category=items[id]["category"],
                research=int(items[id]["research"]),
            )

    def get_item(self, item_id: int) -> Item:
        if item_id in self.items_dict:
            return self.items_dict[item_id]
        return None

    def get_all_items(self) -> list:
        return list(self.items_dict.values())

    def get_all_items_by_category(self, category: str) -> list:
        return [item for item in self.items_dict.values() if item.category == category]

    # Kinda slow
    def get_item_by_internal_name(self, internal_name: str) -> Item:
        return [item for item in self.items_dict.values() if item.internalName == internal_name][0]

    def get_item_by_name(self, name: str) -> Item:
        return [item for item in self.items_dict.values() if item.name == name][0]


with open(ITEMS_JSON_PATH) as f:
    items = json.load(f)
    item_db = ItemDB(items=items)

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
    id: str
    name: str
    internal_name: str
    wiki_url: str
    image_url: str
    category: str
    research_needed: int

    def __str__(self):
        return f"[{self.id}] {self.name} - {self.category} | Needs {self.research_needed} for full research"


class ItemDB:
    def __init__(self, items: list):
        self.items_dict = {}

        for item in items:
            self.items_dict[item["id"]] = Item(
                id=item["id"],
                name=item["name"],
                internal_name=item["internalName"],
                wiki_url=WIKI_ROOT_URL + item["itemUrl"],
                image_url=IMAGE_ROOT_URL + item["imageUrl"],
                category=item["category"],
                research_needed=item["research"],
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
        return [
            item
            for item in self.items_dict.values()
            if item.internal_name == internal_name
        ][0]

    def get_item_by_name(self, name: str) -> Item:
        return [item for item in self.items_dict.values() if item.name == name][0]


with open(ITEMS_JSON_PATH) as f:
    items = json.load(f)
    item_db = ItemDB(items=items)

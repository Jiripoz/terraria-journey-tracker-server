from src.decrypt import (
    decrypt_player_file,
    uint8,
    int32,
    uint32,
    string,
)
from src.item_db import item_db
from global_configs import PLAYER_FILE_PATH
from src.log_setup import logger
from src.recipe_db import recipe_db
import json


def check_easy(item_id, researched):
    item_recipe = recipe_db.recipes_list[item_id]
    ingredients = [x["id"] for x in item_recipe.ingredients]
    if all(y in researched for y in ingredients):
        return True
    return False


def process_data(items_progress, partially_researched, researched, all_items):
    tuplas: list = []
    absolute: int = 0
    research_sum: int = 0
    total_sum: int = 0
    logger.info("process data ok")
    for id in partially_researched:
        item = item_db.get_item(id)
        research_sum += items_progress[id]
        item_progress_percentage = round(
            float(100 * items_progress[id] / item.research_needed), 2
        )
        tuplas.append(
            (
                item_progress_percentage,
                item.name,
                item.research_needed,
                items_progress[id],
            )
        )
    for id in researched:
        absolute += items_progress[id]

    absolute += research_sum

    for id in all_items:
        total_sum += id.research_needed
    return tuplas, absolute, research_sum, total_sum


class Char:
    def __init__(self, path) -> None:
        eraw: bytes = open(path, "rb").read()
        self.bytes: bytes = decrypt_player_file(eraw)
        self.offset: int = 0
        self.all_items = item_db.get_all_items()
        self.items_progress: dict = {}
        self.researched = []
        self.partially_researched = []
        self.easy: dict = {}
        self.absolute: int = 0
        self.total_sum: int = 0
        self.research_sum: int = 0
        self.lista_tuplas: list = []
        self.overview: dict = {}
        self.easy: dict = {}

        self.version = uint32(self.rbytes(4))
        logger.debug(f"version: {self.version}")

        # Skip relogic company name
        self.offset += 24

        self.name = self.read_string()
        logger.debug(f"name: {self.name}")

        # Skip to Spawn point
        self.offset += 2460 + 231

        last_spawn_point = int32(self.rbytes(4))

        # Skip Spawn point and get world name
        while last_spawn_point != -1:
            self.offset += 12

            world_name = self.read_string()
            logger.debug(f"World name: {world_name}")

            last_spawn_point = int32(self.rbytes(4))

        self.offset += 107

        # Get item research progress
        while True:
            item_internal_name = self.read_string()

            if item_internal_name == "":
                logger.debug("Stopped reading Journey")
                break

            research_progress = int32(self.rbytes(4))
            self.offset += 4

            item = item_db.get_item_by_internal_name(item_internal_name)

            if not item:
                logger.error(f"Oooops! We are missing item {item_internal_name}")

            logger.debug(
                f"Researched {research_progress}/{item.research_needed} of {item.name}"
            )
            self.items_progress[item.id] = research_progress
            if item.research_needed == research_progress:
                self.researched.append(item.id)
            if item.research_needed > research_progress:
                self.partially_researched.append(item.id)

        (
            self.lista_tuplas,
            self.absolute,
            self.research_sum,
            self.total_sum,
        ) = process_data(
            self.items_progress,
            self.partially_researched,
            self.researched,
            self.all_items,
        )

    def rbytes(self, n):
        return self.bytes[self.offset : self.offset + n]

    def read_string(self):
        size_bytes = self.rbytes(1)
        size = uint8(size_bytes)

        self.offset += 1

        logger.debug(f"[read_string] Got size {size}")

        str_bytes = self.rbytes(size)
        string_return = string(str_bytes, size)
        logger.debug(f"[read_string] Got string {string_return}")

        self.offset += size

        return string_return

    def get_partial(self):
        partial: dict = {}
        logger.info("eu entro no get partial")
        self.lista_tuplas.sort(key=lambda a: a[0], reverse=True)
        for progress, name, research_needed, item_progress in self.lista_tuplas:
            partial[f"{name}"] = f": {item_progress}/{research_needed} ({progress}%) "
        logger.info(partial, self.lista_tuplas)
        return partial

    def get_easy_researchs(self):
        easy: dict = {}
        all_ids = [x.id for x in self.all_items]
        remaining = [y for y in all_ids if y not in self.researched]
        for id in remaining:
            try:
                if check_easy(id, self.researched):
                    easy[f"{id}"] = item_db.get_item(id).wiki_url
                continue
            except:
                continue
        self.overview["easy"] = len(easy)
        return easy

    def get_progress_overview(self):
        overview: dict = {}
        logger.info(f"overview type is: {type(overview)}")
        progress = round(float(100 * len(self.researched) / len(self.all_items)), 2)
        logger.info(f"o progress existe e é: {progress}")
        overview = {
            "progress": {
                "big": progress,
                "small": len(self.researched),
                "small2": "items researched",
            },
            "not researched": {
                "big": int(len(self.researched) - len(self.all_items)),
                "small": "Items still need to be researched",
            },
            "partially": {
                "big": len(self.partially_researched),
                "small": "Items are partially researched",
            },
            "easy": {
                "big": len(self.easy),
                "small": "Itens can be crafted with things you already researched",
            },
            "absolute": {
                "big": self.absolute,
                "small": round(float(100 * self.absolute / self.total_sum), 2),
            },
        }

        return overview


def get_char(path=None):
    if path == None:
        path = PLAYER_FILE_PATH
    return Char(path)


def fetch_player():
    player = get_char(PLAYER_FILE_PATH)
    partial = player.get_partial()
    easy = player.get_easy_researchs()
    overview = player.get_progress_overview()

    return partial, overview, easy

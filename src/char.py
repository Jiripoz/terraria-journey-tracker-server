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
from src.crafting_station_db import fetch_stations


def check_easy(item_id, researched):
    item_recipe = recipe_db.recipes_list[item_id]
    ingredients = [x["id"] for x in item_recipe.ingredients]
    for y in ingredients:
        if type(y) == list:
            for w in y:
                if w not in researched:
                    return False
        if y not in researched:
            return False

    return True


def get_easy_researchs(all_items, researched):
    easy: list = []
    all_ids = [int(x.id) for x in all_items]
    remaining = [int(y) for y in all_ids if int(y) not in researched]
    for id in remaining:

        try:
            if check_easy(id, researched):
                easy.append(id)
            continue
        except:
            continue
    return easy


def process_data(items_progress, partially_researched, researched, all_items, easy):
    tuplas: list = []
    absolute: int = 0
    research_sum: int = 0
    total_sum: int = 0

    for id in partially_researched:
        item = item_db.get_item(id)
        print(item, id, type(id))
        research_sum += items_progress[id]
        tuplas.append(
            (
                item.id,
                items_progress[id],
                int(id) in easy,
            )
        )

    for id in researched:
        absolute += items_progress[id]

    absolute += research_sum

    for id in all_items:
        total_sum += id.research
    return tuplas, absolute, research_sum, total_sum


def get_partial(lista_tuplas, easy):
    partial: list = []
    lista_tuplas.sort(key=lambda a: a[0], reverse=True)
    for id, item_progress, easy in lista_tuplas:
        partial.append(
            {
                "id": id,
                "item_progress": item_progress,
                "easy": easy,
            }
        )
    logger.info(partial)
    return partial


def get_remaining(all_items, easy, partial, researched):
    not_researched: list = []
    all_ids = [int(x.id) for x in all_items]
    not_researched_id = [id for id in [id for id in all_ids if id not in partial] if id not in researched]

    for id in not_researched_id:
        not_researched.append(
            {
                "id": id,
                "easy": int(id) in easy,
            }
        )

    return not_researched


class Char:
    def __init__(self, path) -> None:
        eraw: bytes = open(path, "rb").read()
        self.bytes: bytes = decrypt_player_file(eraw)
        self.offset: int = 0
        self.all_items = item_db.get_all_items()
        self.items_progress: dict = {}
        self.researched = []
        self.partially_researched = []
        self.absolute: int = 0
        self.total_sum: int = 0
        self.research_sum: int = 0
        self.lista_tuplas: list = []
        self.overview: dict = {}
        self.easy: list = []
        self.partial: list = []
        self.not_researched: list = []

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
            item_internalName = self.read_string()

            if item_internalName == "":
                logger.debug("Stopped reading Journey")
                break

            research_progress = int32(self.rbytes(4))
            self.offset += 4
            item = item_db.get_item_by_internal_name(item_internalName)
            if not item:
                logger.error(f"Oooops! We are missing item {item_internalName}")

            logger.debug(f"Researched {research_progress}/{item.research} of {item.name}")
            self.items_progress[int(item.id)] = research_progress
            if item.research == research_progress:
                self.researched.append(int(item.id))
            if item.research > research_progress:
                self.partially_researched.append(item.id)
        self.easy = get_easy_researchs(self.all_items, self.researched)
        (self.lista_tuplas, self.absolute, self.research_sum, self.total_sum,) = process_data(
            self.items_progress,
            self.partially_researched,
            self.researched,
            self.all_items,
            self.easy,
        )
        self.partial = get_partial(self.lista_tuplas, self.easy)
        self.not_researched = get_remaining(self.all_items, self.easy, self.partial, self.researched)

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

    def get_items_progress(self):
        available = {
            "researched": self.researched,  # ok
            "notInProgress": self.not_researched,  # ok
            "inProgress": self.partial,  # ok
        }
        return available

    def get_overview(self):
        progress = round(float(100 * len(self.researched) / len(self.all_items)), 2)
        overview: dict = {
            "progress": {
                "big": str(progress) + "%",
                "small": len(self.researched),
                "description": "items researched",
            },
            "not_researched": {
                "big": int(len(self.all_items) - len(self.researched)),
                "description": "Items still need to be researched",
            },
            "partially_researched": {
                "big": len(self.partially_researched),
                "description": "Items are partially researched",
            },
            "easy": {
                "big": len(self.easy),
                "description": "Itens can be crafted with things you already researched",
            },
            "absolute": {
                "big": self.absolute,
                "small": str(round(float(100 * self.absolute / self.total_sum), 2)) + "%",
                "description": " of total blocks needed",
            },
        }

        return overview


def get_char(path=None):
    if path == None:
        path = PLAYER_FILE_PATH
    return Char(path)


def fetch_player():
    player = get_char(PLAYER_FILE_PATH)
    items_progress = player.get_items_progress()
    overview = player.get_overview()
    stations = fetch_stations(player.easy, player.items_progress)
    return overview, items_progress, stations

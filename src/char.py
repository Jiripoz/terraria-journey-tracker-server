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


class Char:
    def __init__(self, path) -> None:
        eraw: bytes = open(path, "rb").read()
        self.bytes: bytes = decrypt_player_file(eraw)
        self.offset: int = 0
        self.items_progress: dict = {}
        self.researched = []
        self.partially_researched = []

        logger.debug("Starting parse...")

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

    def print_progress_overview(self):
        logger.info("==============================")
        progress = round(
            float(100 * len(self.researched) / len(item_db.get_all_items())), 2
        )
        logger.info(f"Journey mode progress: {progress}%")
        logger.info(
            f"Researched {len(self.researched)} from {len(item_db.get_all_items())} total items"
        )

        return

    def print_partially_researched(self):
        research_sum: int = 0
        absolute_sum: int = 0
        total_sum: int = 0
        logger.info(f"Items partially researched: ")
        lista_tuplas = []
        for id in self.partially_researched:
            item = item_db.get_item(id)
            research_sum += self.items_progress[id]
            item_progress_percentage = round(
                float(100 * self.items_progress[id] / item.research_needed), 2
            )
            lista_tuplas.append(
                (
                    item_progress_percentage,
                    item.name,
                    item.research_needed,
                    self.items_progress[id],
                )
            )
        for id in self.researched:
            absolute_sum += self.items_progress[id]

        absolute_sum += research_sum

        all_items = item_db.get_all_items()
        for id in all_items:
            total_sum += id.research_needed

        total = round(float(100 * absolute_sum / total_sum), 2)

        lista_tuplas.sort(key=lambda a: a[0], reverse=True)
        for progress, name, research_needed, item_progress in lista_tuplas:
            logger.info(f"{name}: {item_progress}/{research_needed} ({progress}%) ")

        logger.info(f"The sum of items needed to research is {research_sum}")
        logger.info(
            f"The absolute progress of this savefile is: {absolute_sum}/{total_sum} ({total}%)"
        )

        return


def get_char(path=None):
    if path == None:
        path = PLAYER_FILE_PATH
    return Char(path)


# -> print_progress_overview()
# -> print_almost_researched_items()
# print_progress_overview
# - printa quanta coisa foi pesquisada
# - printa quantos % foi pesquisado
# - printa a soma de research needed pra cada item n??o pesquisado (ou seja, quanto falta pra pesquisar todos do jogo)
# print_almost_researched_items
# - printa uma lista de [ID] Nome do Item: x/y

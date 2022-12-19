from src.decrypt import (
    decrypt_player_file,
    uint8,
    int32,
    uint32,
    string,
)
from src.item_db import item_db
from global_configs import PLAYER_FILE_PATH
from log_setup import logger


# decrypt file and get raw bytes


class Char:
    def __init__(self, path) -> None:
        eraw: bytes = open(path, "rb").read()
        self.bytes: bytes = decrypt_player_file(eraw)
        self.offset: int = 0
        self.items_progress: dict = {}

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


def get_char(path=None):
    if path == None:
        path = PLAYER_FILE_PATH
    return Char(path)

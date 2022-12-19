from global_configs import PLAYER_FILE_PATH, VERBOSE
from log_setup import logger
from decrypt import (
    decrypt,
    int8,
    uint8,
    int32,
    uint32,
    boolean,
    btes,
    string,
    struct,
)
from dataclasses import dataclass
from src.item_db import item_db

logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")

# decrypt file and get raw bytes
eraw: bytes = open(PLAYER_FILE_PATH, "rb").read()
raw: bytes = decrypt(eraw)


class Char:
    def __init__(self, bytes) -> None:
        self.bytes = bytes
        self.offset: int = 0

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


c = Char(raw)

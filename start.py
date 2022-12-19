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
    longjohnson,
    shortjohnson,
)
from dataclasses import dataclass
from src.item_db import item_db

logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")

eraw: bytes = open(PLAYER_FILE_PATH, "rb").read()
raw: bytes = decrypt(eraw)


class Char:
    def __init__(self, bytes) -> None:
        self.bytes = bytes
        self.offset: int = 0

        # const version = data.readInt16LE();
        # if(!SUPPORTED_VERSIONS.includes(version)) {
        #     throw new Error(`This library only supports 4.1.2 (and others with the same format) (version id = ${ version })`);
        # }

        logger.debug("Starting parse...")

        self.version = uint32(self.rbytes(4))
        logger.debug(f"version: {self.version}")

        # Skip Relogic bullshit name etc
        self.offset += 24

        # let pos = NAME_OFFSET;
        # [, pos] = read_lpstring(data, pos);
        self.name = self.read_string()
        logger.debug(f"name: {self.name}")

        # // Skip over everything up to the spawn points, all of which is
        # // thankfully static
        self.offset += 2460 + 231  # SPAWN_POINT_OFFSET

        # // Read spawnpoint data until we get to -1, which is the terminator
        # while(data.readInt32LE(pos) !== -1) {
        #     // Skip X + Y + Seed (each are 32 bits)
        #     pos += 12;

        #     // Read the world name
        #     [, pos] = read_lpstring(data, pos);
        # }

        # Read the first spawn point2460
        last_spawn_point = int32(self.rbytes(4))

        while last_spawn_point != -1:
            self.offset += 12

            # Read the world name
            world_name = self.read_string()
            logger.debug(f"World name: {world_name}")

            last_spawn_point = int32(self.rbytes(4))

        # // Skip over the next part - not sure what this data is
        # pos += JOURNEY_OFFSET;

        self.offset += 107

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

        # for(;;) {
        #     let item;
        #     [item, pos] = read_lpstring(data, pos);
        #     if(item.length === 0) {
        #     break;
        #     }

        #     const quantity = data.readInt32LE(pos);
        #     pos += 4;

        #     if(!results[item]) {
        #     console.warn(`Uh oh! Missing item: ${ item }`);
        #     continue;
        #     }

        #     results[item].has = quantity;
        #     results[item].researched = items[item].needed <= quantity;
        # }

        # return results;

    def rbytes(self, n):
        return self.bytes[self.offset : self.offset + n]

    # Reads the next byte. It contains how many bytes we should read.
    def read_string(self):
        size_bytes = self.rbytes(1)
        size = uint8(size_bytes)

        self.offset += 1

        # logger.debug(f"[read_string] Got size {size}")

        str_bytes = self.rbytes(size)
        string_return = string(str_bytes, size)
        logger.debug(f"[read_string] Got string {string_return}")

        self.offset += size

        return string_return


print("Parsing char!")
c = Char(raw)


# Example usage:
# item_1 = item_db.get_item(1)
# logger.info(item_1)

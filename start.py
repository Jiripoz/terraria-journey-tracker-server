from global_configs import PLAYER_FILE_PATH, VERBOSE
from log_setup import logger
from decrypt import decrypt, int8, uint8, int32, uint32, boolean, btes, string, struct
from dataclasses import dataclass

logger.info("starting script")
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")

eraw: bytes = open(PLAYER_FILE_PATH, "rb").read()
raw: bytes = decrypt(eraw)


class Char:
    def __init__(self, bytes) -> None:
        self.bytes = bytes
        self.offset: int = 0
        self.version: int = uint32(self.rbytes(4)[1])
        self.company: str = string(self.rbytes(7)[1], 7)
        self.fileType: int = uint8(self.rbytes(1)[1])
        print(
            "version: %s, company: %s, fileType: %s"
            % (self.version, self.company, self.fileType)
        )
        self.offset += 12

        self.name_lenght: int = uint8(self.rbytes(1)[1])
        self.name: str = string(self.rbytes(self.name_lenght)[1], self.name_lenght)
        self.difficulty: int = int8(self.rbytes(1)[1])
        self.playTime: int = int(struct.unpack("<Q", self.rbytes(8)[1])[0]) / 10000000
        print(
            "name lenght: %s, name: %s, difficulty: %s, play time: %s"
            % (self.name_lenght, self.name, self.difficulty, self.playTime)
        )
        self.offset += 9

        self.HP: int = int32(self.rbytes(4)[1])
        self.HPMax: int = int32(self.rbytes(4)[1])
        self.Mana: int = int32(self.rbytes(4)[1])
        self.ManaMAx: int = int32(self.rbytes(4)[1])
        self.extraAccessory: int = boolean(self.rbytes(1)[1])
        print(
            "current hp: %s, max hp: %s, current mana: %s, max mana: %s, consumed demon heart: %s"
            % (self.HP, self.HPMax, self.Mana, self.ManaMAx, self.extraAccessory)
        )
        self.offset += 1

        self.taxMoney: int = int32(self.rbytes(4)[1])

        self.offset += 23

        self.armor: dict = [
            {"id": int32(self.rbytes(4)[1]), "prefix": uint8(self.rbytes(1)[1])}
            for i in range(3)
        ]
        self.acessories: dict = [
            {"id": int32(self.rbytes(4)[1]), "prefix": uint8(self.rbytes(1)[1])}
            for i in range(6)
        ]
        print("armor: %s\nacessories: %s" % (self.armor, self.acessories))
        self.offset += 10

        self.dye: dict = [
            {"id": int32(self.rbytes(4)[1]), "prefix": uint8(self.rbytes(1)[1])}
            for i in range(12)
        ]
        print("dyes: %s" % self.dye)
        self.offset += 35

        self.inventory = []
        for i in range(58):
            id: int = int32(self.rbytes(4)[1])
            if id >= 5600 or id == 0:
                self.inventory.append({"id": 0})
                self.offset += 6
            else:
                self.inventory.append(
                    {
                        "id": id,
                        "stack": int32(self.rbytes(4)[1]),
                        "prefix": uint8(self.rbytes(1)[1]),
                        "favorites": boolean(self.rbytes(1)[1]),
                    }
                )
        print(self.inventory)

    def rbytes(self, n, get: bool = True):
        if get:
            self.offset += n
            return self.offset - n, self.bytes[self.offset - n : self.offset]
        else:
            return self.bytes[self.offset : self.offset + n]


player = Char(raw)
print(player.version)

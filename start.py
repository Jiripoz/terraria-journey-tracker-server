from global_configs import PLAYER_FILE_PATH, VERBOSE
from log_setup import logger
from decrypt import decrypt, int8, uint8, int32, uint32, boolean, btes, string, struct
from dataclasses import dataclass

logger.info('starting script')
logger.debug(f"PLAYER_FILE_PATH: {PLAYER_FILE_PATH}")
logger.debug(f"VERBOSE: {VERBOSE}")

eraw:bytes = open(PLAYER_FILE_PATH, 'rb').read()
raw:bytes = decrypt(eraw)


class Char:
    
    def __init__(self, bytes) -> None:
        self.bytes = bytes
        self.offset:int=0

    def rbytes(self, n, get:bool=True):
        if get:
            self.offset+=n
            return self.offset-n, self.bytes[self.offset-n:self.offset]
        else: 
            return self.bytes[self.offset:self.offset+n]

    def get_data(self):

        class data:
            version:int = uint32(self.rbytes(4)[1])
            company:str = string(self.rbytes(7)[1], 7)
            fileType:int = uint8(self.rbytes(1)[1])
            print("version: %s, company: %s, fileType: %s"%(version, company, fileType))
            self.offset+=12

            name_lenght:int = uint8(self.rbytes(1)[1])
            name:str = string(self.rbytes(name_lenght)[1], name_lenght)
            difficulty:int = int8(self.rbytes(1)[1])
            playTime:int = int(struct.unpack('<Q', self.rbytes(8)[1])[0])/10000000
            print("name lenght: %s, name: %s, difficulty: %s, play time: %s"%(name_lenght, name, difficulty, playTime))
            self.offset+=9

            HP:int = int32(self.rbytes(4)[1])
            HPMax:int = int32(self.rbytes(4)[1])
            Mana:int = int32(self.rbytes(4)[1])
            ManaMAx:int = int32(self.rbytes(4)[1])
            extraAccessory:int = boolean(self.rbytes(1)[1])
            print("current hp: %s, max hp: %s, current mana: %s, max mana: %s, consumed demon heart: %s"%(HP, HPMax, Mana, ManaMAx, extraAccessory))
            self.offset+=1

            taxMoney:int = int32(self.rbytes(4)[1])

            self.offset+=23

            armor:dict=[{'id':int32(self.rbytes(4)[1]), 'prefix':uint8(self.rbytes(1)[1])} for i in range(3)]
            acessories:dict = [{'id':int32(self.rbytes(4)[1]), 'prefix':uint8(self.rbytes(1)[1])} for i in range(6)]
            print('armor: %s\nacessories: %s'% (armor, acessories))
            self.offset+=10
            
            dye:dict = [{'id': int32(self.rbytes(4)[1]), 'prefix':uint8(self.rbytes(1)[1])} for i in range(12)]
            print('dyes: %s'% dye)
            self.offset+=35

            inventory=[]
            for i in range(58):
                id:int=int32(self.rbytes(4)[1])
                if id>=5600 or id==0:
                    inventory.append({'id':0})
                    self.offset+=6
                else: inventory.append({'id':id, 'stack':int32(self.rbytes(4)[1]), 'prefix':uint8(self.rbytes(1)[1]), 'favorites':boolean(self.rbytes(1)[1])})
            print(inventory)

        return data


Char(raw).get_data()
# for i in d.__annotations__:
#     print(i)

# print([x for x in d.__annotations__])
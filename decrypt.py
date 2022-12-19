import os, subprocess
import struct


key = "6800330079005F006700550079005A00"


def decrypt(raw: bytes) -> bytes:

    with open("tmp", "wb") as f:
        f.write(raw)
        f.close()

    process = subprocess.Popen(
        f"openssl enc -d -nosalt -aes-128-cbc -in tmp -out tmp-out -K {key} -iv {key} -nopad",
        stdout=subprocess.PIPE,
    )
    output, error = process.communicate()

    with open("tmp-out", "rb") as f2:
        data: bytes = f2.read()
        f2.close()

    os.remove("tmp")
    os.remove("tmp-out")

    return data


def uint8(byte: bytes) -> int:
    try:
        return struct.unpack("B", byte)[0]
    except:
        return int(byte)


def int32(byte: bytes) -> int:
    return struct.unpack("i", byte)[0]


def uint32(byte: bytes) -> int:
    return struct.unpack("<I", byte)[0]


def btes(byte: bytes, count: int = 0) -> dict:
    return [byte[i] for i in range(count)]


def string(byte: bytes, count: int = 0) -> str:
    return "".join([chr(i) for i in btes(byte, count)])

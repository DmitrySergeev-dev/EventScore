from time import time


def gen_timestamp_hash() -> str:
    timestamp = int(time()*10000)
    return str(timestamp)

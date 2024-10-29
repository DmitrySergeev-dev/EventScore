from aioredis import Redis


def get_redis_host_and_port():
    host = "0.0.0.0"
    port = 6380
    db = 1
    return dict(host=host, port=port, db=db, decode_responses=True)


r = Redis(**get_redis_host_and_port())

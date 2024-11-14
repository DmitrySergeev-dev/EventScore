from src.bootstrap import bootstrap
from src.service_layer.producers import RedisProducer

messagebus = bootstrap()


def db_uow():
    return messagebus.uow


def redis_broker():
    return RedisProducer()

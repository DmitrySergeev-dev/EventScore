from src.bootstrap import bootstrap

messagebus = bootstrap()


def db_uow():
    return messagebus.uow

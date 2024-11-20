class BaseServiceException(Exception):
    """
    Базовый класс для исключений
    """
    MESSAGE = "Кастомная ошибка"

    def __init__(self, detail=None):
        if not detail:
            detail = self.MESSAGE
        super(Exception, self).__init__(detail)


class WrongMessage(BaseServiceException):
    """Не корректное сообщение"""
    MESSAGE = "Получено сообщение с некорректной структурой!"


class NewsScoreNotFound(BaseServiceException):
    """Событие не найдено"""
    MESSAGE = "Событие не найдено"


class RedisConnectionError(BaseServiceException):
    """Ошибка соединения с Redis"""
    MESSAGE = "Ошибка соединения с Redis. Проверьте настройки."

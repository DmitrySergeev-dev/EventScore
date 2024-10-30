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

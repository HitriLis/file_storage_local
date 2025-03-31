class DomainError(Exception):
    """Базовый класс для ошибок домена"""
    pass


class NotFoundError(DomainError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg


class BadRequestError(DomainError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg

from domain.exceptions.base import DomainError


class UploadFileError(DomainError):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg
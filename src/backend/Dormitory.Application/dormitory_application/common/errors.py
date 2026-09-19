class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class BusinessRuleError(Exception):
    def __init__(self, error_code: str, message: str, status_code: int = 409) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.status_code = status_code

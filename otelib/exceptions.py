"""OTElib exceptions."""


class BaseOtelibException(Exception):
    """A base OTElib exception."""


class ApiError(BaseOtelibException):
    """An API Error Exception"""

    def __init__(self, detail: str, status: int, *args) -> None:
        super().__init__(detail, *args)
        self.detail = detail
        self.status = status

    def __str__(self) -> str:
        return f"APIError: status={self.status} {self.detail}"

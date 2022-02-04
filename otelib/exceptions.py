"""OTElib exceptions."""


class BaseOtelibException(Exception):
    """A base OTElib exception."""


class ApiError(BaseOtelibException):
    """An API Error Exception"""

    def __init__(self, status):
        super().__init__()
        self.status = status

    def __str__(self):
        return f"APIError: status={self.status}"

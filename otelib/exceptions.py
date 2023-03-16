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
        return f"{self.__class__.__name__}: status={self.status} {self.detail}"


class InvalidBackend(BaseOtelibException):
    """The backend does not exist; it is invalid."""


class InvalidStrategy(BaseOtelibException):
    """The strategy type does not exist; it is invalid."""


class PythonBackendException(BaseOtelibException):
    """A generic error has happened in the Python backend."""


class PythonCacheError(PythonBackendException):
    """An error occurred when dealing with the cache in the Python backend."""


class ItemNotFoundInCache(PythonCacheError):
    """An item could not be found in the cache."""

    def __init__(self, detail: str, item: str, *args) -> None:
        super().__init__(detail, *args)
        self.detail = detail
        self.item = item

    def __str__(self) -> str:
        return f" {self.__class__.__name__}: item={self.item!r} {self.detail}"

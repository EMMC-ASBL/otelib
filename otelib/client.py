"""OTE Client."""

from otelib.backends.python.client import OTEPythonClient
from otelib.backends.services.client import OTEServiceClient


class OTEClient:
    def __new__(self, url: str):
        """Initiates an OTEAPI Service client.

        The `url` is the base URL of the OTEAPI Service.
        If 'python' is supplied as the `url` then the python backend will be used
        """
        if url == "python":
            return OTEPythonClient(url)
        else:
            return OTEServiceClient(url)

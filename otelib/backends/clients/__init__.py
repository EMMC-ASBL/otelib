"""OTE Client."""

from otelib.backends.clients.python import OTEPythonClient
from otelib.backends.clients.service import OTEServiceClient


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

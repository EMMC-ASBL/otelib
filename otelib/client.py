"""OTE Client."""
from typing import cast

from otelib.backends.python.client import OTEPythonClient
from otelib.backends.services.client import OTEServiceClient


class OTEClient:
    """The OTEClient object representing a remote OTE REST API.

    Parameters:
        url (str): The base URL of the OTEAPI Service.

    Attributes:
        url (str): The base URL of the OTEAPI Service.

    """

    def __new__(cls, url: str, **kwargs) -> "OTEClient":
        """Initiates an OTEAPI Service client.

        The `url` is the base URL of the OTEAPI Service.
        If 'python' is supplied as the `url` then the python backend will be used
        """
        if url == "python":
            return cast(OTEClient, OTEPythonClient(url, **kwargs))
        return cast(OTEClient, OTEServiceClient(url, **kwargs))

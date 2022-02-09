"""OTElib

A package to interact with the Open Translation Environment (OTE) API.
"""
from .client import OTEClient
from .pipe import Pipe

__all__ = ("OTEClient", "Pipe")

__version__ = "0.0.1"
__author__ = "SINTEF"
__author_email__ = "Team4.0@SINTEF.no"

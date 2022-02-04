"""OTElib

A package to interact with the Open Translation Environment (OTE) API.
"""
from .dataresource import DataResource
from .filter import Filter
from .mapping import Mapping
from .ontotransserver import OntoTransServer
from .pipe import Pipe
from .transformation import Transformation

__all__ = (
    "DataResource",
    "Filter",
    "Transformation",
    "Pipe",
    "Mapping",
    "OntoTransServer",
)

__version__ = "0.0.1"
__author__ = "SINTEF"
__author_email__ = "Team4.0@SINTEF.no"

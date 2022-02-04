"""OTElib

A package to interact with the Open Translation Environment (OTE) API.
"""
from .ontotransserver import OntoTransServer
from .pipe import Pipe

__all__ = ("Pipe", "OntoTransServer")

__version__ = "0.0.1"
__author__ = "SINTEF"
__author_email__ = "Team4.0@SINTEF.no"
